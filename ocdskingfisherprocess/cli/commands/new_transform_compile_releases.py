import ocdskingfisherprocess.cli.commands.base
import ocdskingfisherprocess.database
from ocdskingfisherprocess.transform import TRANSFORM_TYPE_COMPILE_RELEASES


class NewTransformCompileReleasesCLICommand(ocdskingfisherprocess.cli.commands.base.CLICommand):
    command = 'new-transform-compile-releases'

    def configure_subparser(self, subparser):
        self.configure_subparser_for_selecting_existing_collection(subparser)

    def run_command(self, args):
        self.run_command_for_selecting_existing_collection(args)

        if self.collection.deleted_at:
            print("That collection is deleted!")
            return

        id = self.database.get_collection_id(
            self.collection.source_id,
            self.collection.data_version,
            self.collection.sample,
            transform_from_collection_id=self.collection.database_id,
            transform_type=TRANSFORM_TYPE_COMPILE_RELEASES)
        if id:
            print("Already exists! The ID is {}".format(id))
            return

        id = self.database.get_or_create_collection_id(self.collection.source_id,
                                                       self.collection.data_version,
                                                       self.collection.sample,
                                                       transform_from_collection_id=self.collection.database_id,
                                                       transform_type=TRANSFORM_TYPE_COMPILE_RELEASES)

        print("Created! The ID is {}".format(id))
        print("Now run transform-collection with that ID.")
