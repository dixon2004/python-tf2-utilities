from tf2utilities.schema import Schema
from threading import Thread
import time


class TF2:

    def __init__(
            self, 
            api_key: str = None, 
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

        if self.update_time is True: Thread(target=self.updater, daemon=True).start()
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
        if self.api_key is not None:
            raw = {
                "schema": Schema.get_overview(self.api_key) | {"items": Schema.get_items(self.api_key), "paintkits": Schema.get_paint_kits()},
                "items_game": Schema.get_items_game()
            }

            if self.lite:
                del raw["schema"]["originNames"]
                del raw["schema"]["item_sets"]
                del raw["schema"]["item_levels"]
                del raw["schema"]["string_lookups"]

                del raw["items_game"]["game_info"]
                del raw["items_game"]["qualities"]
                del raw["items_game"]["colors"]
                del raw["items_game"]["rarities"]
                del raw["items_game"]["equip_regions_list"]
                del raw["items_game"]["equip_conflicts"]
                del raw["items_game"]["quest_objective_conditions"]
                del raw["items_game"]["item_series_types"]
                del raw["items_game"]["item_collections"]
                del raw["items_game"]["operations"]
                del raw["items_game"]["prefabs"]
                del raw["items_game"]["attributes"]
                del raw["items_game"]["item_criteria_templates"]
                del raw["items_game"]["random_attribute_templates"]
                del raw["items_game"]["lootlist_job_template_definitions"]
                del raw["items_game"]["item_sets"]
                del raw["items_game"]["client_loot_lists"]
                del raw["items_game"]["revolving_loot_lists"]
                del raw["items_game"]["recipes"]
                del raw["items_game"]["achievement_rewards"]
                del raw["items_game"]["attribute_controlled_attached_particles"]
                del raw["items_game"]["armory_data"]
                del raw["items_game"]["item_levels"]
                del raw["items_game"]["kill_eater_score_types"]
                del raw["items_game"]["mvm_maps"]
                del raw["items_game"]["mvm_tours"]
                del raw["items_game"]["matchmaking_categories"]
                del raw["items_game"]["maps"]
                del raw["items_game"]["master_maps_list"]
                del raw["items_game"]["steam_packages"]
                del raw["items_game"]["community_market_item_remaps"]
                del raw["items_game"]["war_definitions"]

            schema = {"time": time.time(), "raw": raw}
            if isinstance(schema, dict): 
                self.schema = Schema(schema)
            else:
                raise Exception("Schema is not a dict.")
