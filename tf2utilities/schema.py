from tf2utilities.webapi import web_request
from tf2utilities.sku import SKU
import requests 
import time
import math
import vdf
import re


exclusive_genuine = {
    "810": 831, # Genuine Red-Tape Recorder
    "811": 832, # Genuine Huo-Long Heater
    "812": 833, # Genuine Flying Guillotine
    "813": 834, # Genuine Neon Annihilator
    "814": 835, # Genuine Triad Trinket
    "815": 836, # Genuine Champ Stamp
    "816": 837, # Genuine Marxman
    "817": 838, # Genuine Human Cannonball
    "30720": 30740, # Genuine Arkham Cowl
    "30721": 30741, # Genuine Firefly
    "30724": 30739 # Genuine Fear Monger
}


exclusive_genuine_reversed = {
    "831": 820, # Red-Tape Recorder
    "832": 811, # Huo-Long Heater
    "833": 812, # Flying Guillotine
    "834": 813, # Neon Annihilator
    "835": 814, # Triad Trinket
    "836": 815, # Champ Stamp
    "837": 816, # Marxman
    "838": 817, # Human Cannonball
    "30740": 30720, # Arkham Cowl
    "30741": 30721, # Firefly
    "30739": 30724 # Fear Monger
}


strangifier_chemistry_set_series = {
    "647": 1,  # All-Father
    "828": 1,  # Archimedes
    "776": 1,  # Bird-Man of Aberdeen
    "451": 1,  # Bonk Boy
    "103": 1,  # Camera Beard
    "446": 1,  # Fancy Dress Uniform
    "541": 1,  # Merc's Pride Scarf
    "733": 1,  # RoBro 3000
    "387": 1,  # Sight for Sore Eyes
    "486": 1,  # Summer Shades
    "386": 1,  # Teddy Roosebelt
    "757": 1,  # Toss-Proof Towel
    "393": 1,  # Villain's Veil
    "30132": 2,  # Blood Banker
    "707": 2,  # Boston Boom-Bringer
    "30073": 2,  # Dark Age Defender
    "878": 2,  # Foppish Physician
    "440": 2,  # Lord Cockswain's Novelty Mutton Chops and Pipe
    "645": 2,  # Outback Intellectual
    "343": 2,  # Professor Speks
    "643": 2,  # Sandvich Safe
    "336": 2,  # Stockbroker's Scarf
    "30377": 3,  # Antarctic Researcher
    "30371": 3,  # Archer's Groundings
    "30353": 3,  # Backstabber's Boomslang
    "30344": 3,  # Bullet Buzz
    "30348": 3,  # Bushi-Dou
    "30361": 3,  # Colonel's Coat
    "30372": 3,  # Combat Slacks
    "30367": 3,  # Cute Suit
    "30357": 3,  # Dark Falkirk Helm
    "30375": 3,  # Deep Cover Operator
    "30350": 3,  # Dough Puncher
    "30341": 3,  # Ein
    "30369": 3,  # Eliminator's Safeguard
    "30349": 3,  # Fashionable Megalomaniac
    "30379": 3,  # Gaiter Guards
    "30343": 3,  # Gone Commando
    "30338": 3,  # Ground Control
    "30356": 3,  # Heat of Winter
    "30342": 3,  # Heavy Lifter
    "30378": 3,  # Heer's Helmet
    "30359": 3,  # Huntsman's Essentials
    "30363": 3,  # Juggernaut Jacket
    "30339": 3,  # Killer's Kit
    "30362": 3,  # Law
    "30345": 3,  # Leftover Trap
    "30352": 3,  # Mustachioed Mann
    "30360": 3,  # Napoleon Complex
    "30354": 3,  # Rat Stompers
    "30374": 3,  # Sammy Cap
    "30366": 3,  # Sangu Sleeves
    "30347": 3,  # Scotch Saver
    "30365": 3,  # Smock Surgeon
    "30355": 3,  # Sole Mate
    "30358": 3,  # Sole Saviors
    "30340": 3,  # Stylish DeGroot
    "30351": 3,  # Teutonic Toque
    "30376": 3,  # Ticket Boy
    "30373": 3,  # Toowoomba Tunic
    "30346": 3,  # Trash Man
    "30336": 3,  # Trencher's Topper
    "30337": 3,  # Trencher's Tunic
    "30368": 3,  # War Goggles
    "30364": 3,  # Warmth Preserver
}


retired_keys = [
    { "defindex": 5049, "name": 'Festive Winter Crate Key' },
    { "defindex": 5067, "name": 'Refreshing Summer Cooler Key' },
    { "defindex": 5072, "name": 'Naughty Winter Crate Key' },
    { "defindex": 5073, "name": 'Nice Winter Crate Key' },
    { "defindex": 5079, "name": 'Scorched Key' },
    { "defindex": 5081, "name": 'Fall Key' },
    { "defindex": 5628, "name": 'Eerie Key' },
    { "defindex": 5631, "name": 'Naughty Winter Crate Key 2012' },
    { "defindex": 5632, "name": 'Nice Winter Crate Key 2012' },
    { "defindex": 5713, "name": 'Spooky Key' }, # Non-Craftable
    { "defindex": 5716, "name": 'Naughty Winter Crate Key 2013' }, # Non-Craftable
    { "defindex": 5717, "name": 'Nice Winter Crate Key 2013' }, # Non-Craftable
    { "defindex": 5762, "name": 'Limited Late Summer Crate Key' }, # Non-Craftable
    { "defindex": 5791, "name": 'Naughty Winter Crate Key 2014' },
    { "defindex": 5792, "name": 'Nice Winter Crate Key 2014' }
]


retired_keys_names = [key.get("name").lower() for key in list(retired_keys)]


class Schema:

    def __init__(self, data: dict) -> None:
        """
        Initializes the Schema class.
        
        Args:
            data (dict): The schema data.
        """
        self.raw = data["raw"] or None
        self.time = data["time"] or time.time()
        self.crate_series_list = self.get_crate_series_list()
        self.munition_crates_list = self.get_munition_crates_list()
        self.weapon_skins_list = self.get_weapon_skins_list()
        self.qualities = self.get_qualities()
        self.effects = self.get_particle_effects()
        self.paintkits = self.get_paint_kits_list()
        self.paints = self.get_paints()


    def get_item_by_name_with_the(self, name: str) -> dict:
        """
        Gets an item by name with "the" in it.

        Args:
            name (str): The name of the item.

        Returns:
            dict: The item object.
        """
        items = self.raw["schema"]["items"]
        
        for item in items:
            if name.lower().replace("the ", "").strip() == item["item_name"].lower().replace("the ", ""):
                if item["item_name"] == "Name Tag" and item["defindex"] == 2093:
                    # skip and let it find Name Tag with defindex 5020
                    continue

                if item["item_quality"] == 0:
                    # skip if Stock Quality
                    continue

                return item

        return None


    def get_sku_from_name(self, name: str) -> str:
        """
        Gets item's SKU from name.
        
        Args:
            name (str): The name of the item.
        
        Returns:
            str: The SKU of the item.
        """
        return SKU.from_object(self.get_item_object_from_name(name))


    def get_item_object_from_name(self, name: str) -> dict:
        """
        Gets an item object from name.

        Args:
            name (str): The name of the item.

        Returns:
            dict: The item object.
        """
        name = name.lower()
        item = {
            "defindex": None,
            "quality": None,
            "craftable": True
        }

        parts = ["strange part:", "strange cosmetic part:", "strange filter:", "strange count transfer tool", "strange bacon grease"]
        if any(part in name for part in parts):
            schema_item = self.get_item_by_item_name(name)
            if not schema_item: 
                return item
            item["defindex"] = schema_item["defindex"]
            item["quality"] = item.get("quality") or schema_item.get("item_quality") # default quality
            return item

        wears = {
            "(factory new)": 1,
            "(minimal wear)": 2,
            "(field-tested)": 3,
            "(well-worn)": 4,
            "(battle scarred)": 5
        }

        for wear in wears:
            if wear in name:
                name = name.replace(wear, "").strip()
                item["wear"] = wears[wear]
                break

        # So far we only have "Strange" as elevated quality, so ignore other qualities.
        is_explicit_elevated_strange = False
        if "strange(e)" in name:
            item["quality2"] = 11
            is_explicit_elevated_strange = True
            name = name.replace("strange(e)", "").strip()

        if "strange" in name:
            item["quality"] = 11
            name = name.replace("strange", "").strip()

        name = name.replace("uncraftable", "non-craftable")
        if "non-craftable" in name:
            name = name.replace("non-craftable", "").strip()
            item["craftable"] = False

        name = name.replace("untradeable", "non-tradable").replace("untradable", "non-tradable").replace("non-tradeable", "non-tradable")
        if "non-tradable" in name:
            name = name.replace("non-tradable", "").strip()
            item["tradable"] = False

        if "unusualifier" in name:
            name = name.replace("unusual ", "").replace(" unusualifier", "").strip()
            item["defindex"] = 9258
            item["quality"] = 5
            schema_item = self.get_item_by_item_name(name)
            item["target"] = schema_item["defindex"] if schema_item else None
            return item

        killstreaks = {
            "professional killstreak": 3,
            "specialized killstreak": 2,
            "killstreak": 1
        }

        for killstreak in killstreaks:
            if killstreak in name:
                name = name.replace(killstreak + " ", "").strip()
                item["killstreak"] = killstreaks[killstreak]
                break

        if "australium" in name and "australium gold" not in name:
            name = name.replace("australium", "").strip()
            item["australium"] = True
        
        if "festivized" in name and "festivized formation" not in name:
            name = name.replace("festivized", "").strip()
            item["festive"] = True

        # Try to find quality name in name
        exception = [
            'haunted ghosts',
            'haunted phantasm jr',
            'haunted phantasm',
            'haunted metal scrap',
            'haunted hat',
            'unusual cap',
            'vintage tyrolean',
            'vintage merryweather',
            'haunted kraken',
            'haunted forever!',
            'haunted cremation',
            "haunted wick"
        ]

        quality_search = name
        for ex in exception:
            if ex in name: 
                quality_search = name.replace(ex, "").strip()
                break

        # Get all qualities
        schema = self.raw["schema"]
        if not any(ex in quality_search for ex in exception):
            # Make sure qualitySearch does not includes in the exception list
            # example: "Haunted Ghosts Vintage Tyrolean" - will skip this
            for quality_c in self.qualities:
                quality = quality_c.lower()
                if quality == "collector's" and "collector's" in quality_search and 'chemistry set' in quality_search:
                    # Skip setting quality if item is Collector's Chemistrt Set
                    continue
                if quality == "community" and quality_search.startswith("community sparkle"):
                    # Skip if starts with Community Sparkle
                    continue
                if quality_search.startswith(quality):
                    name = name.replace(quality, "", 1).strip()
                    item["quality2"] = item.get("quality2") or item.get("quality")
                    item["quality"] = self.qualities[quality_c]
                    break

        # Check for effects
        exclude_atomic = True if any(exclude_name in name for exclude_name in ["bonk! atomic punch", "atomic accolade"]) else False

        for effect_c in self.effects:
            effect = effect_c.lower()
            if effect == "stardust" and "starduster" in name:
                sub = name.replace("stardust", "").strip()
                if "starduster" not in sub:
                    continue
            if effect == "showstopper" and "taunt: " not in name:
                # if the effect is Showstopper and name does not include "Taunt: " or "Shred Alert", skip it
                if "shred alert" not in name: continue
            if effect == "smoking" and (name == "smoking jacket" or "smoking skid lid" in name or name == "the smoking skid lid"):
                # if name only Smoking Jacket or Smoking Skid Lid without effect Smoking, then continue
                if not name.startswith("smoking smoking"): continue
            if effect == "haunted ghosts" and "haunted ghosts" in name and item.get("wear"):
                # if item name includes Haunted Ghosts and wear is defined, skip cosmetic effect and find warpaint for weapon
                continue
            if effect == "pumpkin patch" and "pumpkin patch" in name and item.get("wear"):
                # if item name includes Pumpkin Patch and wear is defined, skip cosmetic effect and find warpaint for weapon
                continue
            if effect == "stardust" and "starduster" in name and item.get("wear"):
                # if item name includes Starduster and wear is defined, skip cosmetic effect and find warpaint for weapon
                continue
            if effect == 'atomic' and ('subatomic' in name or exclude_atomic):
                continue
            if effect == "spellbound" and ("taunt:" in name or "shred alert" in name):
                # skip "Spellbound" for cosmetic if item is a Taunt (to get the correct "Spellbound Aspect")
                continue
            if effect == "accursed" and "accursed apparition" in name:
                # Accursed Apparition never be an unusual
                continue
            if effect == "haunted" and "haunted kraken" in name:
                # Skip Haunted effect if name include Haunted Kraken
                continue
            if effect == "frostbite" and "frostbite bonnet" in name:
                # Skip Frostbite effect if name include Faunted Braken
                continue
            if effect == "frostbite" and "frostbite fit" in name:
                # Skip Frostbite effect if name include Frostbite Fit
                continue

            if effect == "hot": 
                # shotgun # shot to hell
                # plaid potshotter # shot in the dark
                if not item.get("wear"):
                    continue
                elif "hot " not in name and ("shotgun" in name or "shot " in name or "plaid potshotter" in name):
                    # Shotgun
                    # Strange Shotgun
                    # Plaid Potshotter Mk.II Shotgun (Factory New)
                    # Shot to Hell Sniper Rifle (Factory New)
                    # Shot in the Dark Sniper Rifle (Factory New)
                    # Strange Plaid Potshotter Mk.II Shotgun (Factory New)
                    # Strange Shot to Hell Sniper Rifle (Factory New)
                    # Strange Shot in the Dark Sniper Rifle (Factory New)
                    # Strange Cool Shot to Hell Sniper Rifle (Factory New)
                    # Strange Shot in the Dark Sniper Rifle (Factory New)
                    continue
                elif name.startswith("hot "):
                    pass
                else:
                    continue
            if effect == "cool" and not item.get("wear"):
                continue
            if effect in name:
                name = name.replace(effect, "", 1).strip()
                item["effect"] = self.effects[effect_c]
                if  item["effect"] == 4:
                    if item["quality"] is None:
                        item["quality"] = 5
                elif item["quality"] != 5:
                    # will set quality to unusual if undefined, or make it primary, it other quality exists
                    item["quality2"] = item.get("quality2") or item.get("quality")
                    item["quality"] = 5
                break

        if item.get("wear"):
            for paintkit_c in self.paintkits:
                paintkit = paintkit_c.lower()
                if "mk.ii" in name and "mk.ii" not in paintkit:
                    continue
                if "(green)" in name and "(green)" not in paintkit:
                    continue
                if "chilly" in name and 'chilly' not in paintkit:
                    continue
                if paintkit in name:
                    name = name.replace(paintkit, "").replace("|", "").strip()
                    item["paintkit"] = self.paintkits[paintkit_c]
                    if item.get("effect") is not None:
                        if item.get("quality") == 5 and item.get("quality2") == 11:
                            if not is_explicit_elevated_strange:
                                item["quality"] = 11
                                item["quality2"] = None
                            else:
                                item["quality"] = 15
                        elif item.get("quality") == 5 and item.get("quality2") is None:
                            item["quality"] = 15
                    if not item.get("quality"):
                        item["quality"] = 15
                    break

            if "war paint" not in name and "paintkit" in item:
                old_defindex = item["defindex"]
                if 'pistol' in name and str(item['paintkit']) in self.weapon_skins_list["pistol_skins"]:
                    item['defindex'] = self.weapon_skins_list["pistol_skins"][str(item['paintkit'])]
                elif 'rocket launcher' in name and str(item['paintkit']) in self.weapon_skins_list["rocket_launcher_skins"]:
                    item['defindex'] = self.weapon_skins_list["rocket_launcher_skins"][str(item['paintkit'])]
                elif 'medi gun' in name and str(item['paintkit']) in self.weapon_skins_list["medicgun_skins"]:
                    item['defindex'] = self.weapon_skins_list["medicgun_skins"][str(item['paintkit'])]
                elif 'revolver' in name and str(item['paintkit']) in self.weapon_skins_list["revolver_skins"]:
                    item['defindex'] = self.weapon_skins_list["revolver_skins"][str(item['paintkit'])]
                elif 'stickybomb launcher' in name and str(item['paintkit']) in self.weapon_skins_list["stickybomb_skins"]:
                    item['defindex'] = self.weapon_skins_list["stickybomb_skins"][str(item['paintkit'])]
                elif 'sniper rifle' in name and str(item['paintkit']) in self.weapon_skins_list["sniper_rifle_skins"]:
                    item['defindex'] = self.weapon_skins_list["sniper_rifle_skins"][str(item['paintkit'])]
                elif 'flame thrower' in name and str(item['paintkit']) in self.weapon_skins_list["flame_thrower_skins"]:
                    item['defindex'] = self.weapon_skins_list["flame_thrower_skins"][str(item['paintkit'])]
                elif 'minigun' in name and str(item['paintkit']) in self.weapon_skins_list["minigun_skins"]:
                    item['defindex'] = self.weapon_skins_list["minigun_skins"][str(item['paintkit'])]
                elif 'scattergun' in name and str(item['paintkit']) in self.weapon_skins_list["scattergun_skins"]:
                    item['defindex'] = self.weapon_skins_list["scattergun_skins"][str(item['paintkit'])]
                elif 'shotgun' in name and str(item['paintkit']) in self.weapon_skins_list["shotgun_skins"]:
                    item['defindex'] = self.weapon_skins_list["shotgun_skins"][str(item['paintkit'])]
                elif 'smg' in name and str(item['paintkit']) in self.weapon_skins_list["smg_skins"]:
                    item['defindex'] = self.weapon_skins_list["smg_skins"][str(item['paintkit'])]
                elif 'grenade launcher' in name and str(item['paintkit']) in self.weapon_skins_list["grenade_launcher_skins"]:
                    item['defindex'] = self.weapon_skins_list["grenade_launcher_skins"][str(item['paintkit'])]
                elif 'wrench' in name and str(item['paintkit']) in self.weapon_skins_list["wrench_skins"]:
                    item['defindex'] = self.weapon_skins_list["wrench_skins"][str(item['paintkit'])]
                elif 'knife' in name and str(item['paintkit']) in self.weapon_skins_list["knife_skins"]:
                    item['defindex'] = self.weapon_skins_list["knife_skins"][str(item['paintkit'])]
                if old_defindex != item["defindex"]: return item

        if "(paint: " in name:
            name = name.replace("(paint: ", "").replace(")", "").strip()
            for paint_c in self.paints:
                paint = paint_c.lower()
                if paint in name:
                    name = name.replace(paint, "").strip()
                    item["paint"] = self.paints[paint_c]
                    break

        if "kit fabricator" in name and item["killstreak"] > 1:
            name = name.replace("kit fabricator", "").strip()
            item["defindex"] = 20003 if item['killstreak'] > 2 else 20002
            if name != "":
                # Generic Fabricator Kit
                schema_item = self.get_item_by_item_name(name)
                if not schema_item: return item
                item["target"] = schema_item["defindex"]
                item["quality"] = item.get("quality") or schema_item.get("item_quality") # default quality
            if not item.get("quality"): item["quality"] = 6
            item["output"] = 6526 if item["killstreak"] > 2 else 6523
            item["outputQuality"] = 6
            
        if ("strangifier chemistry set" not in name or "collector's" in name) and "chemistry set" in name:
            name = name.replace("collector's", "").replace("chemistry set", "").strip()
            item["defindex"] = 20007 if "festive" in name and "a rather festive tree" not in name else 20006
            schema_item = self.get_item_by_item_name(name)
            if not schema_item: return item
            item["output"] = schema_item["defindex"]
            item["outputQuality"] = 14
            item["quality"] = item.get("quality") or schema_item.get("item_quality") # default quality

        if "strangifier chemistry set" in name:
            name = name.replace("strangifier chemistry set", "").strip()
            schema_item = self.get_item_by_item_name(name)
            if not schema_item: return item
            # Standardize defindex for Strangifier Chemistry Set
            item["defindex"] = 20000
            item["target"] = schema_item["defindex"]
            item["quality"] = 6
            item["output"] = 6522
            item["outputQuality"] = 6

        if "strangifier" in name:
            name = name.replace("strangifier", "").strip()
            # Standardize to use only 6522
            item["defindex"] = 6522
            schema_item = self.get_item_by_item_name(name)
            if not schema_item: return name
            item["target"] = schema_item["defindex"]
            item["quality"] = item.get("quality") or schema_item.get("item_quality") # default quality

        if "kit" in name and item.get("killstreak"):
            name = name.replace("kit", "").strip()
            if item["killstreak"] == 1:
                item["defindex"] = 6527 # most new items only use this defindex, thus we ignore specific defindex ks1
            elif item["killstreak"] == 2:
                item["defindex"] = 6523
            elif item["killstreak"] == 3:
                item["defindex"] = 6526
            # If Generis Kit, ignore this
            if name != "":
                schema_item = self.get_item_by_item_name(name)
                if not schema_item: return item
                item["target"] = schema_item["defindex"]
            if not item.get("quality"): item["quality"] = 6

        if item.get("defindex"): return item

        if isinstance(item.get("paintkit"), int) and "war paint" in name:
            name = f"Paintkit {item['paintkit']}"
            if not item.get("quality"): item["quality"] = 15
            items = schema["items"]
            for it in items:
                if it["name"] == name:
                    item["defindex"] = it["defindex"]
                    break

        else:
            name = name.replace(" series ", "").replace(" series#", " #")
            if "salvaged mann co. supply crate #" in name:
                item["crateseries"] = int(name[32:])
                item["defindex"] = 5068
                item["quality"] = 6
                return item
            
            elif "select reserve mann co. supply crate #" in name:
                item["defindex"] = 5660
                item["crateseries"] = 60
                item["quality"] = 6
                return item

            elif "mann co. supply crate #" in name:
                crateseries = int(name[23:])
                if crateseries in {1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75}:
                    item["defindex"] = 5022
                elif crateseries in {2, 4, 8, 11, 14, 17, 20, 24, 27, 32, 37, 42, 44, 49, 56, 71, 76}:
                    item["defindex"] = 5041
                elif crateseries in {5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77}:
                    item["defindex"] = 5045
                item["crateseries"] = crateseries
                item["quality"] = 6
                return item

            elif "mann co. supply munition #" in name:
                crateseries = int(name[26:])
                item["defindex"] = self.munition_crates_list.get(str(crateseries))
                item["crateseries"] = crateseries
                item["quality"] = 6
                return item

            number = None

            if "#" in name:
                without_number = name.split('#')[0]
                number = name[len(without_number) + 1:].strip()
                name = name.split('#')[0].strip()

            if name in retired_keys_names:
                for retired_key in retired_keys:
                    if retired_key["name"].lower() == name:
                        item["defindex"] = retired_key["defindex"]
                        item["quality"] = item.get("quality") or 6
                        return item

            schema_item = self.get_item_by_name_with_the(name)
            if not schema_item: return item
            item["defindex"] = schema_item["defindex"]
            item["quality"] = item.get("quality") if item.get("quality") is not None else schema_item.get("item_quality") # default quality

            # Fix defindex for Exclusive Genuine items
            if item["quality"] == 1:
                if str(item["defindex"]) in exclusive_genuine.keys():
                    item["defindex"] = exclusive_genuine[str(item['defindex'])]

            if schema_item["item_class"] == "supply_crate":
                item["crateseries"] = self.crate_series_list.get(str(item["defindex"])) or None
            
            elif schema_item["item_class"] != "supply_crate" and number is not None:
                item["craftnumber"] = number

        return item


    def get_item_by_defindex(self, defindex: int) -> dict:
        """
        Gets schema item by defindex.
        
        Args:
            defindex (int): The defindex of the item.
            
        Returns:
            dict: The item object.
        """
        items = self.raw["schema"]["items"]
        items_count = len(items)

        start = 0
        end = items_count - 1
        iter_lim = math.ceil(math.log2(items_count)) + 2

        while start <= end:
            if iter_lim <= 0: break # use fallback search
            iter_lim = iter_lim - 1
            mid = math.floor((start + end) / 2)
            if items[mid]["defindex"] < defindex:
                start = mid + 1
            elif items[mid]["defindex"] > defindex:
                end = mid -1
            else:
                return items[mid]

        for item in items:
            if item["defindex"] == defindex: return item

        return None


    def get_item_by_item_name(self, name: str) -> dict:
        """
        Gets schema item by item name.

        Args:
            name (str): The name of the item.
        
        Returns:
            dict: The item object.
        """
        items = self.raw["schema"]["items"]

        for item in items:
            if name.lower() == item["item_name"].lower():
                if item["item_name"] == "Name Tag" and item["defindex"] == 2093:
                    # skip and let it find name tag with defindex 5020
                    continue

                if item["item_quality"] == 0:
                    # skip if stock quality
                    continue

                return item
        
        return None


    def get_item_by_sku(self, sku: str) -> dict:
        """
        Gets schema item by SKU.
        
        Args:
            sku (str): The SKU of the item.
        
        Returns:
            dict: The item object.
        """
        return self.get_item_by_defindex(SKU.from_string(sku)["defindex"])


    def get_attribute_by_defindex(self, defindex: int) -> dict:
        """
        Gets schema attribute by defindex.
        
        Args:
            defindex (int): The defindex of the attribute.
            
        Returns:
            dict: The attribute object.
        """
        attributes = self.raw["schema"]["attributes"]
        attributes_count = len(attributes)
        
        start = 0
        end = attributes_count - 1
        iter_lim = math.ceil(math.log2(attributes_count)) + 2

        while start <= end:
            if iter_lim <= 0: break # use fallback search
            mid = math.floor((start + end) / 2)
            if attributes[mid]["defindex"] < defindex:
                start = mid + 1
            elif attributes[mid]["defindex"] > defindex:
                end = mid - 1
            else:
                return attributes[mid]

        for attribute in attributes:
            if attribute["defindex"] == defindex: return attribute

        return None


    def get_quality_by_id(self, id: int) -> str:
        """
        Gets quality name by id.
        
        Args:
            id (int): The id of the quality.
        
        Returns:
            str: The name of the quality.
        """
        qualities = self.raw["schema"]["qualities"]
        
        for type in qualities:
            if type not in qualities: continue

            if qualities[type] == id: return self.raw["schema"]["qualityNames"][type]
        
        return None

    
    def get_quality_by_name(self, name: str) -> int:
        """
        Gets quality id by name.
        
        Args:
            name (str): The name of the quality.
            
        Returns:
            int: The id of the quality.
        """
        quality_names = self.raw["schema"]["qualityNames"]
        
        for type in quality_names:
            if not quality_names.get(type): continue

            if name.lower() == quality_names[type].lower(): return self.raw["schema"]["qualities"][type]
        
        return None

    
    def get_effect_by_id(self, id: int) -> str:
        """
        Gets effect name by id.
        
        Args:
            id (int): The id of the effect.
            
        Returns:
            str: The name of the effect.
        """
        particles = self.raw["schema"]["attribute_controlled_attached_particles"]
        particles_count = len(particles)

        start = 0
        end = particles_count -1
        iter_lim = math.ceil(math.log2(particles_count)) + 2

        while start <= end:
            if iter_lim <= 0: break # use fallback search
            mid = math.floor((start + end) / 2)
            if particles[mid]["id"] < id: 
                start = mid + 1
            elif particles[mid]["id"] > id:
                end = mid -1
            else:
                return particles[mid]["name"]

        for effect in particles:
            if effect["id"] == id: return effect["name"]

        return None


    def get_effect_id_by_name(self, name: str) -> int:
        """
        Gets effect id by name.
        
        Args:
            name (str): The name of the effect.
        
        Returns:
            int: The id of the effect.
        """
        particles = self.raw["schema"]["attribute_controlled_attached_particles"]
        
        for effect in particles:
            if name.lower() == effect["name"].lower(): return effect["id"]

        return None


    def get_skin_by_id(self, id: int) -> str:
        """
        Gets skin name by id.
        
        Args:
            id (int): The id of the skin.
        
        Returns:
            str: The name of the skin.
        """
        paintkits = self.raw["schema"]['paintkits']

        if not paintkits.get(str(id)): return None

        return paintkits[str(id)]


    def get_skin_by_name(self, name: str) -> int:
        """
        Gets skin id by name.
        
        Args:
            name (str): The name of the skin.
        
        Returns:
            int: The id of the skin.
        """
        paintkits = self.raw["schema"]['paintkits']

        for id in paintkits:
            if not paintkits.get(id): continue

            if name.lower() == paintkits[id].lower(): return int(id)

        return None


    def get_unusual_effects(self) -> list:
        """
        Gets the name and id of unusual effects.
        
        Returns:
            list: The list of unusual effects.
        """
        unusual_effects = []

        for effect in self.raw["schema"]["attribute_controlled_attached_particles"]:
            unusual_effects.append({"name": effect["name"], "id": effect["id"]})
        
        return unusual_effects


    def get_paint_name_by_decimal(self, decimal: int) -> str:
        """
        Gets paint name by decimal numeral system.
        
        Args:
            decimal (int): The decimal numeral system of the paint.
            
        Returns:
            str: The name of the paint.
        """
        if decimal == 5801378: return "Legacy Paint"

        paint_cans = []
        for item in self.raw["schema"]["items"]:
            if "Paint Can" in item["name"] and item["name"] != "Paint Can":
                paint_cans.append(item)

        for paint in paint_cans:
            if paint["attributes"] is None: continue

            for attr in paint["attributes"]:
                if attr["value"] == decimal: return paint["item_name"]
        
        return None


    def get_paint_decimal_by_name(self, name: str) -> int:
        """
        Gets paint decimal numeral system by name.
        
        Args:
            name (str): The name of the paint.
        
        Returns:
            int: The decimal numeral system of the paint.
        """
        if name == "Legacy Paint": return 5801378

        paint_cans = []
        for item in self.raw["schema"]["items"]:
            if "Paint Can" in item["name"] and item["name"] != "Paint Can":
                paint_cans.append(item)
        
        for paint in paint_cans:
            if paint["attributes"] is None: continue

            if name.lower() == paint["item_name"].lower(): return paint["attributes"][0]["value"]

        return None


    def get_paints(self) -> dict:
        """
        Gets the name and partial SKU for painted items.
        
        Returns:
            dict: The name and partial SKU of painted items.
        """
        paint_cans = []
        for item in self.raw["schema"]["items"]:
            if "Paint Can" in item["name"] and item["name"] != "Paint Can":
                paint_cans.append(item)

        to_object = {}
        
        for paint_can in paint_cans:
            if paint_can["attributes"] is None: continue

            to_object[paint_can["item_name"]] = int(paint_can['attributes'][0]['value'])

        to_object["Legacy Paint"] = "5801378"

        return to_object


    def get_paintable_item_defindexes(self) -> list:
        """
        Gets an array of paintable items' defindex.
        
        Returns:
            list: The array of paintable items' defindex.
        """
        paintable_item_defindexes = []
        
        for item in self.raw["schema"]["items"]:
            if "capabilities" in item and "paintable" in item["capabilities"] and item["capabilities"]["paintable"] is True: 
                paintable_item_defindexes.append(item["defindex"])

        return paintable_item_defindexes

    
    def get_strange_parts(self) -> dict:
        """
        Gets the name and partial SKU for strange parts items.
        
        Returns:
            dict: The name and partial SKU of strange parts items.
        """
        parts_to_exclude = {
            'Ubers',
            'Kill Assists',
            'Sentry Kills',
            'Sodden Victims',
            'Spies Shocked',
            'Heads Taken',
            'Humiliations',
            'Gifts Given',
            'Deaths Feigned',
            'Buildings Sapped',
            'Tickle Fights Won',
            'Opponents Flattened',
            'Food Items Eaten',
            'Banners Deployed',
            'Seconds Cloaked',
            'Health Dispensed to Teammates',
            'Teammates Teleported',
            'KillEaterEvent_UniquePlayerKills',
            'Points Scored',
            'Double Donks',
            'Teammates Whipped',
            'Wrangled Sentry Kills',
            'Carnival Kills',
            'Carnival Underworld Kills',
            'Carnival Games Won',
            'Contracts Completed',
            'Contract Points',
            'Contract Bonus Points',
            'Times Performed',
            'Kills and Assists during Invasion Event',
            'Kills and Assists on 2Fort Invasion',
            'Kills and Assists on Probed',
            'Kills and Assists on Byre',
            'Kills and Assists on Watergate',
            'Souls Collected',
            'Merasmissions Completed',
            'Halloween Transmutes Performed',
            'Power Up Canteens Used',
            'Contract Points Earned',
            'Contract Points Contributed To Friends'
        }

        to_object = {}

        # Filter out built-in parts and also filter repeated "Kills"
        parts = []
        for type in self.raw["schema"]["kill_eater_score_types"]:
            if type["type_name"] not in parts_to_exclude and type["type"] not in [0, 97]: parts.append(type)

        for part in parts:
            to_object[part["type_name"]] = f"sp{part['type']}"

        return to_object


    def get_craftable_weapons_schema(self) -> list:
        """
        Gets an array of item objects for craftable weapons.
        
        Returns:
            list: The array of item objects for craftable weapons.
        """
        weapons_to_exclude = {
            # Exclude these weapons
            266, # Horseless Headless Horsemann's Headtaker
            452, # Three-Rune Blade
            466, # Maul
            474, # Conscientious Objector
            572, # Unarmed Combat
            574, # Wanga Prick
            587, # Apoco-Fists
            638, # Sharp Dresser
            735, # Sapper
            736, # Sapper
            737, # Construction PDA
            851, # AWPer Hand
            880, # Freedom Staff
            933, # Ap-Sap
            939, # Bat Outta Hell
            947, # Quäckenbirdt
            1013, # Ham Shank
            1152, # Grappling Hook
            30474 # Nostromo Napalmer
        }

        craftable_weapons = []
        for item in self.raw["schema"]["items"]:
            if item["defindex"] not in weapons_to_exclude and item["item_quality"] == 6 and item.get("craft_class") == "weapon": 
                craftable_weapons.append(item)

        return craftable_weapons


    def get_weapons_for_crafting_by_class(self, char_class: str) -> list:
        """
        Gets an array of SKU for craftable weapons by class used for crafting.
        
        Args:
            char_class (str): The character class.
        
        Returns:
            list: The array of SKU for craftable weapons by class used for crafting.
        """
        if char_class not in {'Scout', 'Soldier', 'Pyro', 'Demoman', 'Heavy', 'Engineer', 'Medic', 'Sniper', 'Spy'}:
            raise Exception(f'Entered class "{char_class}" is not a valid character class.\nValid character classes (case sensitive): "Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy".')
        
        weapons = []
        for item in self.get_craftable_weapons_schema():
            if char_class in item["used_by_classes"]: weapons.append(f'{item["defindex"]};6')

        return weapons

    
    def get_craftable_weapons_for_trading(self) -> list:
        """
        Gets an array of SKU for craftable weapons used for trading.
        
        Returns:
            list: The array of SKU for craftable weapons used for trading.
        """
        weapons = []
        for item in self.get_craftable_weapons_schema():
            weapons.append(f"{item['defindex']};6")

        return weapons


    def get_uncraftable_weapons_for_trading(self) -> list:
        """
        Gets an array of SKU for non-craftable weapons used for trading.
        
        Returns:
            list: The array of SKU for non-craftable weapons used for trading.
        """
        weapons = []
        for item in self.get_craftable_weapons_schema():
            if item["defindex"] not in [48, 349, 1178, 1179, 1180, 1181, 1190]: 
                weapons.append(f"{item['defindex']};6;uncraftable")

        return weapons


    def get_crate_series_list(self) -> dict:
        """
        Gets the name and series number of crates.
        
        Returns:
            dict: The name and series number of crates.
        """
        items = self.raw["schema"]["items"]

        crate_series = {}
        for item in items:
            if "attributes" in item:
                attributes = item["attributes"]
                for attr in attributes:
                    if attr["name"] == "set supply crate series": 
                        crate_series.update({str(item["defindex"]): int(attr["value"])})
                        break

        items = self.raw["items_game"]["items"]
        defindexes = [x for x in items]

        for defindex in defindexes:
            if items[defindex].get("static_attrs") and items[defindex]["static_attrs"].get("set supply crate series"):
                crate_series.update({str(defindex): int(items[defindex]["static_attrs"]["set supply crate series"])})

        items = None
        return crate_series


    def get_qualities(self) -> dict:
        """
        Gets the name and id of qualities.
        
        Returns:
            dict: The name and id of qualities.
        """
        schema = self.raw["schema"]
        qualities = {}
        for quality_type in schema["qualities"]:
            qualities.update({str(schema["qualityNames"][quality_type]): int(schema["qualities"][quality_type])})

        return qualities


    def get_particle_effects(self) -> dict:
        """
        Gets the name and id of particle effects.
        
        Returns:
            dict: The name and id of particle effects.
        """
        previous = ""
        effects = {}
        for particle in self.raw["schema"]["attribute_controlled_attached_particles"]:
            particle_name = particle["name"]
            if particle_name != previous:
                effects.update({str(particle_name): int(particle["id"])})
                if particle_name == "Eerie Orbiting Fire":
                    del effects["Orbiting Fire"]
                    effects.update({"Orbiting Fire": 33})

                if particle_name == "Nether Trail":
                    del effects["Ether Trail"]
                    effects.update({"Ether Trail": 103})

                if particle_name == "Refragmenting Reality":
                    del effects["Fragmenting Reality"]
                    effects.update({"Fragmenting Reality": 141})
            previous = particle_name  

        # id 326 has an empty name causing things to break
        effects.pop('', None)
        return effects


    def get_paint_kits_list(self) -> dict:
        """
        Gets the name and id of paint kits.
        
        Returns:
            dict: The name and id of paint kits.
        """
        schema = self.raw["schema"]
        return {schema["paintkits"][paintkit]: int(paintkit) for paintkit in schema["paintkits"]}


    def check_existence(self, item: dict) -> bool:
        """
        Checks if the item exists in the schema.
        
        Args:
            item (dict): The item object.
        
        Returns:
            bool: True if the item exists, False otherwise.
        """
        schema_item = self.get_item_by_defindex(item["defindex"])
        if not schema_item: return False

        # Items with default quality
        if schema_item["item_quality"] in {0, 3, 5, 11}:
            # default Normal (Stock items), Vintage (1156), Unusual (266, 267), and Strange (655) items
            if item.get("quality") != schema_item["item_quality"]: return False

        # Exclusive Genuine items
        if ((item.get("quality") != 1 and item["defindex"] in [exclusive_genuine_reversed.get(egr) for egr in exclusive_genuine_reversed]) or 
            (item.get("quality") == 1 and item["defindex"] in [exclusive_genuine.get(eg) for eg in exclusive_genuine])):
            # if quality not 1 AND item.defindex is the one that should be Genuine only, OR
            # if quality is 1 AND item.defindex is the one that can be any quality, return null.
            return False

        # Retired keys
        for retired_key in retired_keys:
            if retired_key.get("defindex") == item["defindex"]:
                if item["defindex"] in [5713, 5716, 5717, 5762]:
                    if item.get("craftable") is True:
                        return False
                elif item["defindex"] not in [5791, 5792]:
                    if item.get("craftable") is False:
                        return False

        # Crates/Cases
        def have_other_attribute_for_crate_or_case():
            return (
                item["quality"] != 6 or
                item["killstreak"] != 0 or
                item["australium"] is not False or
                item["effect"] is not None or
                item["festive"] is not False or
                item["paintkit"] is not None or
                item["wear"] is not None or
                item["quality2"] is not None or
                item["craftnumber"] is not None or
                item["target"] is not None or
                item["output"] is not None or
                item["outputQuality"] is not None or
                item["paint"] is not None
            )
        if schema_item["item_class"] == "supply_crate" and item.get("crateseries") is None:
            if item["defindex"] not in {5739, 5760, 5737, 5738}:
                # If not seriesless, return false
                # Mann Co. Director's Cut Reel, Mann Co. Audition Reel, and Mann Co. Stockpile Crate
                return False
            # Unlocked Creepy 5763, 5764, 5765, 5766, 5767, 5768, 5769, 5770, 5771
            # Unlocked Crates 5850, 5851, 5852, 5853, 5854, 5855, 5856, 5857, 5858, 5860
            if have_other_attribute_for_crate_or_case(): return False
        if item.get("crateseries"):
            # Run a check if the input item is actually exist or not for crates/cases
            if have_other_attribute_for_crate_or_case(): return False
            if schema_item["item_class"] != "supply_crate":
                # Not a crate or case
                return False
            elif (item["crateseries"] not in {1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75, 2, 4, 8, 11, 14, 17, 20, 24, 27,
                32, 37, 42, 44, 49, 56, 71, 76, 5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77, 30,
                40, 50, 82, 83, 84, 85, 90, 91, 92, 103}):
                # if item["crateseries"] not included in the single defindex multiple series crate:
                if item["crateseries"] not in [self.crate_series_list[crates_series] for crates_series in self.crate_series_list]:
                    # if item["crateseries"] is not included in the crate_series_list, does not exist.
                    return False
                # Check for specific crates/cases
                if item["crateseries"] != self.crate_series_list[item["defindex"]]: return False
            elif not (
                (item["crateseries"] in {1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75} and item["defindex"] == 5022) or
                (item["crateseries"] in {2, 4, 8, 11, 14, 17, 20, 24, 27, 32, 37, 42, 44, 49, 56, 71, 76} and item["defindex"] == 5041) or
                (item["crateseries"] in {5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77} and item["defindex"] == 5045) or
                (item["crateseries"] in {30, 40, 50} and item["defindex"] == 5068) or
                (self.munition_crates_list.get(str(item["crateseries"])) and item["defindex"] == self.munition_crates_list.get(str(item["crateseries"])))):
                # if single defindex multiple series crate don't match, does not exist
                return False

        return True


    def get_name(
            self, 
            item: dict, 
            proper: bool = True, 
            use_pipe_for_skin: bool = False, 
            scm_format: bool = False
            ) -> str:
        """
        Gets the name of an item with specific attributes.
        
        Args:
            item (dict): The item object.
            proper (bool, optional): The proper name of the item. Defaults to True.
            use_pipe_for_skin (bool, optional): The pipe for skin. Defaults to False.
            scm_format (bool, optional): The Steam Community Market format. Defaults to False.

        Returns:
            str: The name of the item.
        """
        schema_item = self.get_item_by_defindex(item["defindex"])
        if schema_item is None: return None

        name = ""

        if not scm_format and item.get("tradable") is False: name = "Non-Tradable "

        if not scm_format and item.get("craftable") is False: name += "Non-Craftable "

        if item.get("quality2"):
            # Elevated quality
            name += self.get_quality_by_id(item["quality2"]) + ("(e)" if not scm_format and (item["wear"] is not None or item["paintkit"] is not None) else "") + " "

        if ((item["quality"] != 6 and item["quality"] != 15 and item["quality"]  != 5) or
            (item["quality"]  == 5 and not item.get("effect")) or
            (item["quality"] == 6 and item.get("quality2")) or
            (item["quality"] == 5 and scm_format) or 
            schema_item["item_quality"] == 5):
            # If the quality is Unique (and is Elevated quality) 
            # or not Unique, Decorated, or Unusual, 
            # or if the quality is Unusual but it does not have an effect, 
            # or if the item can only be unusual, 
            # or if it's unusual and Steam Community Market format,
            # then add the quality
            name += self.get_quality_by_id(item["quality"]) + " "

        if not scm_format and item.get("effect"): name += self.get_effect_by_id(item["effect"]) + " "

        if item.get("festive") is True: name += "Festivized "

        if item.get("killstreak") and item["killstreak"] > 0: name += ['Killstreak', 'Specialized Killstreak', 'Professional Killstreak'][item["killstreak"] - 1] + ' '

        if item.get("target"): name += self.get_item_by_defindex(item["target"])["item_name"] + " "

        if item.get("outputQuality") and item["outputQuality"] != 6: name = self.get_quality_by_id(item["outputQuality"]) + " " + name

        if item.get("output"): name += self.get_item_by_defindex(item["output"])["item_name"] + " "

        if item.get("australium") is True: name += "Australium "

        if item.get("paintkit") and type(item["paintkit"]) == int: name += self.get_skin_by_id(item["paintkit"]) + (" " if use_pipe_for_skin is False else " | ")

        if proper is True and name == "" and schema_item["proper_name"] is True: name = "The "

        for retired_key in retired_keys:
            if retired_key.get("defindex") == item["defindex"]:
                name += retired_key["name"]
                break
        else:
            name += schema_item["item_name"]

        if item.get("wear"): name += ' (' + ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle Scarred'][item["wear"] - 1] + ')'

        if item.get("crateseries"):
            if "attributes" in schema_item and schema_item["attributes"][0]["class"] == "supply_crate_series":
                has_attr = True
            else:
                has_attr = False
            if scm_format:
                if has_attr:
                    name += " Series %23" + str(item["crateseries"])
                # Else we don't need to add #number
            else:
                name += " #" + str(item["crateseries"])
        elif item.get("craftnumber"):
            name += ' #' + str(item["craftnumber"])

        if not scm_format and item.get("paint"): name += f" (Paint: {self.get_paint_name_by_decimal(item['paint'])})"

        if scm_format and schema_item["item_name"] == "Chemistry Set" and item.get("output") == 6522:
            if item.get("target") and strangifier_chemistry_set_series.get(str(item["target"])):
                name += f" Series %23{strangifier_chemistry_set_series.get(str(item['target']))}"

        if scm_format and item.get('wear') is not None and item.get('effect') is not None and item.get('quality') == 15:
            # Need to add "Unusual" for Unusual Skins for Steam Community Market
            # for item quality 15
            name = 'Unusual ' + name

        return name


    def get_name_from_sku(self, sku: str) -> str:
        """
        Gets the name of an item with specific SKU.
        
        Args:
            sku (str): The SKU of the item.
            
        Returns:
            str: The name of the item.
        """
        if self.test_sku(sku) is True:
            return self.get_name(SKU.from_string(sku))
        else:
            return None

    
    def test_sku(self, sku: str) -> bool:
        """
        Checks if the SKU is valid or not.
        
        Args:
            sku (str): The SKU of the item.
        
        Returns:
            bool: True if the SKU is valid, False otherwise."""
        if bool(re.match(
            "^(\d+);([0-9]|[1][0-5])(;((uncraftable)|(untrad(e)?able)|(australium)|(festive)|(strange)|((u|pk|td-|c|od-|oq-|p)\d+)|(w[1-5])|(kt-[1-3])|(n((100)|[1-9]\d?))))*?$", sku)):
            return True

    
    def get_munition_crates_list(self) -> dict:
        """
        Gets the name and defindex of munition crates.
        
        Returns:
            dict: The name and defindex of munition crates.
        """
        munition_crates_list = {}
        items = self.raw["schema"]["items"]
        for item in items:
            if item["item_name"] == "Mann Co. Supply Munition":
                munition_crates_list.update({str(item["attributes"][0]["value"]): int(item["defindex"])})

        return munition_crates_list


    def get_weapon_skins_list(self) -> dict:
        """
        Gets the name and defindex of weapon skins.
        
        Returns:
            dict: The name and defindex of weapon skins.
        """
        items = self.raw["items_game"]["items"]
        pistol_skins = {}
        rocket_launcher_skins = {}
        medicgun_skins = {}
        revolver_skins = {}
        stickybomb_skins = {}
        sniper_rifle_skins = {}
        flame_thrower_skins = {}
        minigun_skins = {}
        scattergun_skins = {}
        shotgun_skins = {}
        smg_skins = {}
        wrench_skins = {}
        grenade_launcher_skins = {}
        knife_skins = {}
        for item in items:
            if items[item].get("prefab"):
                if items[item]["prefab"] == "paintkit_weapon_pistol":
                    pistol_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_rocketlauncher":
                    rocket_launcher_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_medigun":
                    medicgun_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_revolver":
                    revolver_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_stickybomb_launcher":
                    stickybomb_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_sniperrifle":
                    sniper_rifle_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_flamethrower":
                    flame_thrower_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_minigun":
                    minigun_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_scattergun":
                    scattergun_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_shotgun":
                    shotgun_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_smg":
                    smg_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_wrench":
                    wrench_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_grenadelauncher":
                    grenade_launcher_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_knife":
                    knife_skins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})

        weapon_skins_list = {
            "pistol_skins": pistol_skins,
            "rocket_launcher_skins": rocket_launcher_skins,
            "medicgun_skins": medicgun_skins,
            "revolver_skins": revolver_skins,
            "stickybomb_skins": stickybomb_skins,
            "sniper_rifle_skins": sniper_rifle_skins,
            "flame_thrower_skins": flame_thrower_skins,
            "minigun_skins": minigun_skins,
            "scattergun_skins": scattergun_skins,
            "shotgun_skins": shotgun_skins,
            "smg_skins": smg_skins,
            "wrench_skins": wrench_skins,
            "grenade_launcher_skins": grenade_launcher_skins,
            "knife_skins": knife_skins
        }
        return weapon_skins_list


    @staticmethod
    def get_overview(api_key : str) -> dict:
        """
        Gets the schema overview.
        
        Args:
            api_key (str): The Steam Web API key.
        
        Returns:
            dict: The schema overview.
        """
        input = {
            "key": api_key,
            "language": "en"
        }
        overview = web_request('GET', 'GetSchemaOverview', 'v0001', input)["result"]
        del overview["status"]
        return overview


    @staticmethod
    def get_items(api_key: str) -> list:
        """
        Gets the schema items.
        
        Args:
            api_key (str): The Steam Web API key.
        
        Returns:
            list: The schema items.
        """
        return get_all_schema_items(api_key)


    @staticmethod
    def get_paint_kits() -> dict:
        """
        Gets the name and id of paint kits.
        
        Returns:
            dict: The name and id of paint kits.
        """
        response = requests.get('https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/resource/tf_proto_obj_defs_english.txt', timeout=10)
        if response.status_code == 200:
            parsed = vdf.loads(response.text)
            protodefs = parsed["lang"]["Tokens"]
            paintkits = []
            for protodef in protodefs:
                if protodef not in protodefs: continue
                parts = protodef[0:protodef.index(' ')].split('_')
                if len(parts) != 3: continue
                type = parts[0]
                if type != "9": continue
                DEF = parts[1]
                name = protodefs[protodef]
                if name.startswith(DEF + ':'): continue
                paintkits.append({"id": DEF, "name": name})
            paintkits = sorted(paintkits, key=lambda x:int(x["id"]))
            paintkits_obj = {}
            for paint_kit in paintkits:
                paint_kit_name = paint_kit["name"]
                if paint_kit_name not in [paintkits_obj[paintkit] for paintkit in paintkits_obj]:
                    paintkits_obj[paint_kit["id"]] = paint_kit["name"]
            return paintkits_obj
        else:
            raise Exception("Failed to get paintkits.")


    @staticmethod
    def get_items_game() -> dict:
        """
        Gets the items game.
        
        Returns:
            dict: The items game.
        """
        response = requests.get('https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/scripts/items/items_game.txt', timeout=10)
        if response.status_code == 200:
            return vdf.loads(response.text)["items_game"]
        else:
            raise Exception("Failed to get items game.")


    def to_json(self) -> dict:
        """
        Creates a data object used for initializing the class.
        
        Returns:
            dict: The data object used for initializing the class.
        """
        return {"time": time.time(), "raw": self.raw}


def get_all_schema_items(api_key: str) -> list:
    """
    Recursively gets all schema items.
    
    Args:
        api_key (str): The Steam Web API key.
    
    Returns:
        list: The list of schema items.
    """
    input = {
        "key": api_key,
        "language": "en"
    }
    result = web_request('GET', 'GetSchemaItems', 'v0001', input)
    items = result["result"]["items"]
    while "next" in result["result"]:
        input = {
            "key": api_key,
            "language": "en",
            "start": result["result"]["next"]
        }
        result = web_request('GET', 'GetSchemaItems', 'v0001', input)
        items = items + result["result"]["items"]
        
    return items
