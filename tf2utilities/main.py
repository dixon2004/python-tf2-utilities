import time
from threading import Thread

from tf2utilities.schema import Schema


class TF2:

    def __init__(
            self, 
            api_key: str = "", 
            auto_update: bool = False, 
            update_time: int = 24 * 60 * 60, 
            lite: bool = False
            ) -> None:
        """
        Initializes the TF2 class.
        
        Args:
            api_key (str): The Steam API key.
            auto_update (bool): Whether to automatically update the schema.
            update_time (int): The time in seconds to wait before updating the schema.
            lite (bool): Whether to use the lite version of the schema.
        """
        self.api_key = api_key
        self.auto_update = auto_update
        self.update_time = update_time
        self.schema = None
        self.lite = lite

        if self.auto_update: Thread(target=self.updater, daemon=True).start()
        if self.schema is None: self.get_schema()


    def updater(self) -> None:
        """
        Starts the schema updater.
        """
        while True:
            self.get_schema()
            time.sleep(self.update_time)


    def get_schema(self) -> None:
        """
        Gets the schema from the TF2 API.
        """
        if self.api_key != "":
            raw = {
                "schema": Schema.get_overview(self.api_key) | {"items": Schema.get_items(self.api_key), "paintkits": Schema.get_paint_kits()},
                "items_game": Schema.get_items_game()
            }

            if self.lite:
                del raw["schema"]["originNames"]
                del raw["schema"]["item_sets"]
                del raw["schema"]["item_levels"]
                del raw["schema"]["string_lookups"]

            self.schema = Schema({"time": time.time(), "raw": raw})
