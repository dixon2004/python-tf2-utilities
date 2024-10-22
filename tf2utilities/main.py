import requests.exceptions
from tf2utilities.schema import Schema
from threading import Thread
import time


class TF2:
    def __init__(self, apiKey=None, autoUpdate=False, updateTime=24 * 60 * 60, lite=False):
        self.apiKey = apiKey
        self.autoUpdate = autoUpdate
        self.updateTime = updateTime
        self.schema = None
        self.lite = lite
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
            try:
                while 1:
                    raw = {
                        "schema": Schema.getOverview(self.apiKey) | {"items": Schema.getItems(self.apiKey), "paintkits": Schema.getPaintKits()},
                        "items_game": Schema.getItemsGame()
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
                    break
            except:
                time.sleep(10)
