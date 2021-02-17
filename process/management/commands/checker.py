import json
import traceback

from django.db import transaction

from process.exceptions import AlreadyExists
from process.management.commands.base.worker import BaseWorker
from process.models import (Collection, CollectionFile, CollectionNote,
                            ProcessingStep)
from process.processors.checker import check_collection_file


class Command(BaseWorker):

    worker_name = "checker"

    consume_keys = ["file_worker"]

    def __init__(self):
        super().__init__(self.worker_name)

    def process(self, channel, method, properties, body):
        # parse input message
        input_message = json.loads(body.decode("utf8"))
        try:

            self._debug("Received message {}".format(input_message))

            collection_file = CollectionFile.objects.select_related("collection").get(
                pk=input_message["collection_file_id"]
            )

            if "check" in collection_file.collection.steps:
                try:
                    with transaction.atomic():
                        check_collection_file(collection_file)
                except AlreadyExists:
                    self._exception("Checks already calculated for collection file {}".format(collection_file))
                    self._save_note(
                        collection_file.collection,
                        CollectionNote.Codes.WARNING,
                        "Checks already calculated for collection file {}".format(collection_file),
                    )

                self._info("Checks calculated for collection file {}".format(collection_file))
            else:
                self._info("Collection file {} is not checkable. Skip.".format(collection_file))

            self._deleteStep(ProcessingStep.Types.CHECK, collection_file_id=collection_file.id)
        except Exception:
            self._exception("Something went wrong when processing {}".format(body))
            try:
                collection = Collection.objects.get(collectionfile__id=input_message["collection_file_id"])
                self._save_note(
                    collection,
                    CollectionNote.Codes.ERROR,
                    "Unable to process collection file id {} \n{}".format(
                        input_message["collection_file_id"], traceback.format_exc()
                    ),
                )
            except Exception:
                self._exception("Failed saving collection note")

        channel.basic_ack(delivery_tag=method.delivery_tag)
