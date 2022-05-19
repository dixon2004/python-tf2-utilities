from tf2utilities.schema import Schema
from threading import Thread
import time


class TF2:
    def __init__(self, apiKey=None, autoUpdate=False, updateTime=24 * 60 * 60):
        self.apiKey = apiKey
        self.autoUpdate = autoUpdate
        self.updateTime = updateTime
        self.schema = None
        # Starts schema updater if autopricer is True
        if self.autoUpdate is True: Thread(target=self.updater, daemon=True).start()
        if self.schema is None: self.getSchema()


    # Schema updater
    def updater(self):
        while True:
            self.getSchema()
            time.sleep(self.updateTime)


    # Gets the schema from the TF2 API
    def getSchema(self):
        if self.apiKey is not None:
            raw = {
                "schema": Schema.getOverview(self.apiKey) | {"items": Schema.getItems(self.apiKey), "paintkits": Schema.getPaintKits()},
                "items_game": Schema.getItemsGame()
            }
            schema = {"time": time.time(), "raw": raw}
            if isinstance(schema, dict): 
                self.schema = Schema(schema)
            else:
                raise Exception("Schema is not a dict.")
