import datetime

import sqlalchemy as sa
from ocdskit.upgrade import upgrade_10_11

from ocdskingfisherprocess.database import DatabaseStore
from ocdskingfisherprocess.transform.base import BaseTransform


class Upgrade10To11Transform(BaseTransform):

    def process(self):
        # Is Source Collection still here and not deleted?
        if not self.source_collection or self.source_collection.deleted_at:
            return

        # Is destination deleted?
        if self.destination_collection.deleted_at:
            return

        # Have we already marked this transform as finished?
        if self.destination_collection.store_end_at:
            return

        # Do the work ...
        for file_model in self.database.get_all_files_in_collection(self.source_collection.database_id):
            self.process_file(file_model)
            # Early return?
            if self.run_until_timestamp and self.run_until_timestamp < datetime.datetime.utcnow().timestamp():
                return

        # We maybe mark the transform as finished here
        # There is a race condition we have to be careful off
        # * Collection starts being downloaded, 100 files downloaded and saved
        # * Transform starts
        # * Transform loads list of 100 files into memory
        # * Transform takes a while to process all 100 files
        # * In that time, 10 final files are downloaded and saved and source collection is marked as ended
        # * Now we can't mark the destination collection as closed because we haven't processed the 10 final files!
        # Fortunately, because this check is "if self.source_collection.store_end_at" and
        #   because "self.source_collection" is loaded into memory right at start, this race condition can't occur.
        # But leaving comment as warning to others that order of loading things into memory is important
        if self.source_collection.store_end_at:
            self.database.mark_collection_store_done(self.destination_collection.database_id)

    def process_file(self, file_model):
        for file_item_model in self.database.get_all_files_items_in_file(file_model):
            self.process_file_item(file_model, file_item_model)
            # Early return?
            if self.run_until_timestamp and self.run_until_timestamp < datetime.datetime.utcnow().timestamp():
                return

    def process_file_item(self, file_model, file_item_model):
        with self.database.get_engine().begin() as connection:
            release_rows = connection.execute(
                self.database.release_table.select().where(
                    self.database.release_table.c.collection_file_item_id == file_item_model.database_id)
            )

            release_ids = [x['id'] for x in release_rows]

        for release_id in release_ids:
            if not self.has_release_id_been_done(release_id):
                self.process_release_id(file_model, file_item_model, release_id)
            # Early return?
            if self.run_until_timestamp and self.run_until_timestamp < datetime.datetime.utcnow().timestamp():
                return

        del release_rows

        with self.database.get_engine().begin() as connection:
            record_rows = connection.execute(
                self.database.record_table.select().where(
                    self.database.record_table.c.collection_file_item_id == file_item_model.database_id)
            )

            record_ids = [x['id'] for x in record_rows]

        for record_id in record_ids:
            if not self.has_record_id_been_done(record_id):
                self.process_record_id(file_model, file_item_model, record_id)
            # Early return?
            if self.run_until_timestamp and self.run_until_timestamp < datetime.datetime.utcnow().timestamp():
                return

    def process_release_id(self, file_model, file_item_model, release_id):
        with self.database.get_engine().begin() as connection:
            s = sa.sql.select([self.database.release_table]) \
                .where(self.database.release_table.c.id == release_id)
            result = connection.execute(s)
            release_row = result.fetchone()

        package = self.database.get_package_data(release_row.package_data_id)
        package['releases'] = [self.database.get_data(release_row.data_id)]
        package = upgrade_10_11(package)

        def add_status(database, connection):
            connection.execute(database.transform_upgrade_1_0_to_1_1_status_release_table.insert(), {
                'source_release_id': release_row.id,
            })

        package_data = {}
        for key, value in package.items():
            if key != 'releases':
                package_data[key] = value

        with DatabaseStore(database=self.database, collection_id=self.destination_collection.database_id,
                           file_name=file_model.filename, number=file_item_model.number,
                           url=file_model.url, before_db_transaction_ends_callback=add_status,
                           allow_existing_collection_file_item_table_row=True) as store:

            store.insert_release(package['releases'][0], package_data)

    def process_record_id(self, file_model, file_item_model, record_id):
        with self.database.get_engine().begin() as connection:
            s = sa.sql.select([self.database.record_table]) \
                .where(self.database.record_table.c.id == record_id)
            result = connection.execute(s)
            record_row = result.fetchone()

        package = self.database.get_package_data(record_row.package_data_id)
        package['records'] = [self.database.get_data(record_row.data_id)]
        package = upgrade_10_11(package)

        def add_status(database, connection):
            connection.execute(database.transform_upgrade_1_0_to_1_1_status_record_table.insert(), {
                'source_record_id': record_row.id,
            })

        package_data = {}
        for key, value in package.items():
            if key != 'records':
                package_data[key] = value

        with DatabaseStore(database=self.database, collection_id=self.destination_collection.database_id,
                           file_name=file_model.filename, number=file_item_model.number,
                           url=file_model.url, before_db_transaction_ends_callback=add_status,
                           allow_existing_collection_file_item_table_row=True) as store:

            store.insert_record(package['records'][0], package_data)

    def has_release_id_been_done(self, release_id):
        with self.database.get_engine().begin() as connection:
            s = sa.sql.select([self.database.transform_upgrade_1_0_to_1_1_status_release_table]) \
                .where(
                    self.database.transform_upgrade_1_0_to_1_1_status_release_table.c.source_release_id == release_id
                )
            result = connection.execute(s)
            return result.rowcount == 1

    def has_record_id_been_done(self, record_id):
        with self.database.get_engine().begin() as connection:
            s = sa.sql.select([self.database.transform_upgrade_1_0_to_1_1_status_record_table]) \
                .where(self.database.transform_upgrade_1_0_to_1_1_status_record_table.c.source_record_id == record_id)
            result = connection.execute(s)
            return result.rowcount == 1
