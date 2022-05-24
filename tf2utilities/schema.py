from tf2utilities.webapi import WebRequest
from tf2utilities.sku import SKU
import requests 
import time
import math
import vdf
import re


# munitionCrate = {
#     "82": 5734,
#     "83": 5735,
#     "84": 5742,
#     "85": 5752,
#     "90": 5781,
#     "91": 5802,
#     "92": 5803,
#     "103": 5859
# }


# pistolSkins = {
# 	"0": 15013,
# 	"18": 15018,
# 	"35": 15035,
# 	"41": 15041,
# 	"46": 15046,
# 	"56": 15056,
# 	"61": 15061,
# 	"63": 15060,
# 	"69": 15100,
# 	"70": 15101,
# 	"74": 15102,
# 	"78": 15126,
# 	"81": 15148
# }


# rocketLauncherSkins = {
# 	"1": 15014,
# 	"6": 15006,
# 	"28": 15028,
# 	"43": 15043,
# 	"52": 15052,
# 	"57": 15057,
# 	"60": 15081,
# 	"69": 15104,
# 	"70": 15105,
# 	"76": 15129,
# 	"79": 15130,
# 	"80": 15150
# }


# medicgunSkins = {
# 	"2": 15010,
# 	"5": 15008,
# 	"25": 15025,
# 	"39": 15039,
# 	"50": 15050,
# 	"65": 15078,
# 	"72": 15097,
# 	"76": 15120,
# 	"78": 15121,
# 	"79": 15122,
# 	"81": 15145,
# 	"83": 15146
# }


# revolverSkins = {
# 	"3": 15011,
# 	"27": 15027,
# 	"42": 15042,
# 	"51": 15051,
# 	"63": 15064,
# 	"64": 15062,
# 	"65": 15063,
# 	"72": 15103,
# 	"76": 15127,
# 	"77": 15128,
# 	"81": 15149
# }


# stickybombSkins = {
# 	"4": 15012,
# 	"8": 15009,
# 	"24": 15024,
# 	"38": 15038,
# 	"45": 15045,
# 	"48": 15048,
# 	"60": 15082,
# 	"62": 15083,
# 	"63": 15084,
# 	"68": 15113,
# 	"76": 15137,
# 	"78": 15138,
# 	"81": 15155
# }


# sniperRifleSkins = {
# 	"7": 15007,
# 	"14": 15000,
# 	"19": 15019,
# 	"23": 15023,
# 	"33": 15033,
# 	"59": 15059,
# 	"62": 15070,
# 	"64": 15071,
# 	"65": 15072,
# 	"76": 15135,
# 	"66": 15111,
# 	"67": 15112,
# 	"78": 15136,
# 	"82": 15154
# }


# flameThrowerSkins = {
# 	"9": 15005,
# 	"17": 15017,
# 	"30": 15030,
# 	"34": 15034,
# 	"49": 15049,
# 	"54": 15054,
# 	"60": 15066,
# 	"61": 15068,
# 	"62": 15067,
# 	"66": 15089,
# 	"67": 15090,
# 	"76": 15115,
# 	"80": 15141
# }


# minigunSkins = {
# 	"10": 15004,
# 	"20": 15020,
# 	"26": 15026,
# 	"31": 15031,
# 	"40": 15040,
# 	"55": 15055,
# 	"61": 15088,
# 	"62": 15087,
# 	"63": 15086,
# 	"70": 15098,
# 	"73": 15099,
# 	"76": 15123,
# 	"77": 15125,
# 	"78": 15124,
# 	"84": 15147
# }


# scattergunSkins = {
# 	"11": 15002,
# 	"15": 15015,
# 	"21": 15021,
# 	"29": 15029,
# 	"36": 15036,
# 	"53": 15053,
# 	"61": 15069,
# 	"63": 15065,
# 	"69": 15106,
# 	"72": 15107,
# 	"74": 15108,
# 	"76": 15131,
# 	"83": 15157,
# 	"85": 15151
# }


# shotgunSkins = {
# 	"12": 15003,
# 	"16": 15016,
# 	"44": 15044,
# 	"47": 15047,
# 	"60": 15085,
# 	"72": 15109,
# 	"76": 15132,
# 	"78": 15133,
# 	"86": 15152
# }


# smgSkins = {
# 	"13": 15001,
# 	"22": 15022,
# 	"32": 15032,
# 	"37": 15037,
# 	"58": 15058,
# 	"65": 15076,
# 	"69": 15110,
# 	"79": 15134,
# 	"81": 15153
# }


# wrenchSkins = {
# 	"60": 15074,
# 	"61": 15073,
# 	"64": 15075,
# 	"75": 15114,
# 	"77": 15140,
# 	"78": 15139,
# 	"82": 15156
# }


# grenadeLauncherSkins = {
# 	"60": 15077,
# 	"63": 15079,
# 	"67": 15091,
# 	"68": 15092,
# 	"76": 15116,
# 	"77": 15117,
# 	"80": 15142,
# 	"84": 15158
# }


# knifeSkins = {
# 	"64": 15080,
# 	"69": 15094,
# 	"70": 15095,
# 	"71": 15096,
# 	"77": 15119,
# 	"78": 15118,
# 	"81": 15143,
# 	"82": 15144
# }


exclusiveGenuine = {
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


exclusiveGenuineReversed = {
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


retiredKeys = [
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


retiredKeysNames = [key.get("name").lower() for key in list(retiredKeys)]


class Schema:
    def __init__(self, data):
        self.raw = data["raw"] or None
        self.time = data["time"] or time.time()
        self.crateSeriesList = self.getCrateSeriesList()
        self.munitionCratesList = self.getMunitionCratesList()
        self.getWeaponSkinsList = self.getWeaponSkinsList()


    def getItemByNameWithThe(self, name):
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


    # Gets sku
    def getSkuFromName(self, name):
        return SKU.fromObject(self.getItemObjectFromName(name))


    # Gets sku item object
    def getItemObjectFromName(self, name):
        name = name.lower()
        item = {
            "defindex": None,
            "quality": None,
            "craftable": True
        }

        parts = ["strange part:", "strange cosmetic part:", "strange filter:", "strange count transfer tool", "strange bacon grease"]
        if any(part in name for part in parts):
            schemaItem = self.getItemByItemName(name)
            if not schemaItem: 
                return item
            item["defindex"] = schemaItem["defindex"]
            item["quality"] = item["quality"] or schemaItem["item_quality"] # default quality
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

        if "strange" in name:
            if item.get("wear"):
                item["quality2"] = 11
            else:
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
            schemaItem = self.getItemByItemName(name)
            item["target"] = schemaItem["defindex"] if schemaItem else None
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
        
        if "festivized" in name:
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
            'vintage merryweather'
        ]

        qualitySearch = name
        for ex in exception:
            if ex in name: 
                qualitySearch = name.replace(ex, "").strip()
                break

        # Get all qualities
        schema = self.raw["schema"]
        qualities = {}
        for qualityType in schema["qualities"]:
            qualities.update({str(schema["qualityNames"][qualityType].lower()): int(schema["qualities"][qualityType])})
        if not any(ex in qualitySearch for ex in exception):
            # Make sure qualitySearch does not includes in the exception list
            # example: "Haunted Ghosts Vintage Tyrolean" - will skip this
            for quality in qualities:
                if quality == "collector's" and "collector's" in qualitySearch and 'chemistry set' in qualitySearch:
                    # Skip setting quality if item is Collector's Chemistrt Set
                    continue
                if quality == "community" and qualitySearch.startswith("community sparkle"):
                    # Skip if starts with Community Sparkle
                    continue
                if qualitySearch.startswith(quality):
                    name = name.replace(quality, "").strip()
                    item["quality2"] = item["quality"]
                    item["quality"] = qualities[quality]
                    break

        # Check for effects
        previous = ""
        effects = {}
        for particle in schema["attribute_controlled_attached_particles"]:
            particleName = particle["name"].lower()
            if particleName != previous:
                effects.update({str(particleName): int(particle["id"])})
                if particleName == "eerie orbiting fire":
                    del effects["orbiting fire"]
                    effects.update({"orbiting fire": 33})

                if particleName == "nether trail":
                    del effects["ether trail"]
                    effects.update({"ether trail": 103})

                if particleName == "refragmenting reality":
                    del effects["fragmenting reality"]
                    effects.update({"fragmenting reality": 141})
            previous = particleName  

        excludeAtomic = True if any(excludeName in name for excludeName in ["bonk! atomic punch", "atomic accolade"]) else False

        for effect in effects:
            if effect == "showstopper" and "taunt: " not in name:
                # if the effect is Showstopper and name does not include "Taunt: " or "Shred Alert", skip it
                if "shred alert" not in name: continue
            if effect == "smoking" and (name == "smoking jacket" or "smoking skid lid" in name or name == "the smoking skid lid"):
                # if name only Smoking Jacket or Smoking Skid Lid without effect Smoking, then continue
                if not name.startswith("smoking smoking"): continue
            if effect == "haunted ghosts" and "haunted ghosts" in name and item.get("wear"):
                # if item name includes Haunted Ghosts and wear is defined, skip cosmetic effect and find warpaint for weapon
                continue
            if effect == 'atomic' and ('subatomic' in name or excludeAtomic):
                continue
            if effect == "spellbound" and ("taunt:" in name or "shred alert" in name):
                # skip "Spellbound" for cosmetic if item is a Taunt (to get the correct "Spellbound Aspect")
                continue
            if effect == "accursed" and "accursed apparition" in name:
                # Accursed Apparition never be an unusual
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
                item["effect"] = effects[effect]
                if  item["effect"] == 4:
                    if item["quality"] is None:
                        item["quality"] = 5
                elif item["quality"] != 5:
                    # will set quality to unusual if undefined, or make it primary, it other quality exists
                    item["quality2"] = item.get("quality2") or item["quality"]
                    item["quality"] = 5
                break

        if item.get("wear"):
            paintkits = {schema["paintkits"][paintkit].lower(): int(paintkit) for paintkit in schema["paintkits"]}
            for paintkit in paintkits:
                if "mk.ii" in name and "mk.ii" not in paintkit:
                    continue
                if paintkit in name:
                    name = name.replace(paintkit, "").replace("|", "").strip()
                    item["paintkit"] = paintkits[paintkit]
                    if not item.get("effect"):
                        if item.get("quality2") == 11:
                            item["quality"] = 11
                            item["quality2"] = None
                        else:
                            item["quality"] = 15
                    else:
                        if item.get("quality2") == 11:
                            item["quality"] == 11
                            item["quality2"] = None
                    break

            if "war paint" not in name:
                oldDefindex = item["defindex"]
                if (int(item["paintkit"]) >= 0 and int(item["paintkit"]) <= 66) or (int(item["paintkit"]) >= 68 and int(item["paintkit"]) <= 75) or (int(item["paintkit"]) >= 77 and int(item["paintkit"]) <= 84) or int(item["paintkit"]) in [86, 67, 85, 76]:
                    # Special Skins, but still need to filter because not everything is special
                    # TODO: Investigate whether this also the reason we have two Strange variants for skins?
                    if 'pistol' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["pistolSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["pistolSkins"][str(item['paintkit'])]
                    elif 'rocket launcher' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["rocketLauncherSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["rocketLauncherSkins"][str(item['paintkit'])]
                    elif 'medi gun' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["medicgunSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["medicgunSkins"][str(item['paintkit'])]
                    elif 'revolver' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["revolverSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["revolverSkins"][str(item['paintkit'])]
                    elif 'stickybomb launcher' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["stickybombSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["stickybombSkins"][str(item['paintkit'])]
                    elif 'sniper rifle' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["sniperRifleSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["sniperRifleSkins"][str(item['paintkit'])]
                    elif 'flame thrower' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["flameThrowerSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["flameThrowerSkins"][str(item['paintkit'])]
                    elif 'minigun' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["minigunSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["minigunSkins"][str(item['paintkit'])]
                    elif 'scattergun' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["scattergunSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["scattergunSkins"][str(item['paintkit'])]
                    elif 'shotgun' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["shotgunSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["shotgunSkins"][str(item['paintkit'])]
                    elif 'smg' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["smgSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["smgSkins"][str(item['paintkit'])]
                    elif 'grenade launcher' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["grenadeLauncherSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["grenadeLauncherSkins"][str(item['paintkit'])]
                    elif 'wrench' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["wrenchSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["wrenchSkins"][str(item['paintkit'])]
                    elif 'knife' in name:
                        if str(item['paintkit']) in self.getWeaponSkinsList["knifeSkins"]:
                            item['defindex'] = self.getWeaponSkinsList["knifeSkins"][str(item['paintkit'])]
                if oldDefindex != item["defindex"]: return item

        if "(paint: " in name:
            name = name.replace("(paint: ", "").replace(")", "").strip()
            paints = {
                'indubitably green': 7511618,
                "zepheniah's greed": 4345659,
                "noble hatter's violet": 5322826,
                'color no. 216-190-216': 14204632,
                'a deep commitment to purple': 8208497,
                'mann co. orange': 13595446,
                'muskelmannbraun': 10843461,
                'peculiarly drab tincture': 12955537,
                'radigan conagher brown': 6901050,
                'ye olde rustic colour': 8154199,
                'australium gold': 15185211,
                'aged moustache grey': 8289918,
                'an extraordinary abundance of tinge': 15132390,
                'a distinctive lack of hue': 1315860,
                'team spirit': 12073019,
                'pink as hell': 16738740,
                'a color similar to slate': 3100495,
                'drably olive': 8421376,
                'the bitter taste of defeat and lime': 3329330,
                "the color of a gentlemann's business pants": 15787660,
                'dark salmon injustice': 15308410,
                "operator's overalls": 4732984,
                'waterlogged lab coat': 11049612,
                'balaclavas are forever': 3874595,
                'an air of debonair': 6637376,
                'the value of teamwork': 8400928,
                'cream spirit': 12807213,
                "a mann's mint": 12377523,
                'after eight': 2960676,
                'legacy paint': 5801378
            }
            for paint in paints:
                if paint in name:
                    name = name.replace(paint, "").strip()
                    item["paint"] = paints[paint]
                    break

        if "kit fabricator" in name and item["killstreak"] > 1:
            name = name.replace("kit fabricator", "").strip()
            item["defindex"] = 20003 if item['killstreak'] > 2 else 20002
            if name != "":
                # Generic Fabricator Kit
                schemaItem = self.getItemByItemName(name)
                if not schemaItem: return item
                item["target"] = schemaItem["defindex"]
                item["quality"] = item["quality"] or schemaItem["item_quality"] # default quality
            if not item.get("quality"): item["quality"] = 6
            item["output"] = 6526 if item["killstreak"] > 2 else 6523
            item["outputQuality"] = 6
            
        if ("strangifier chemistry set" not in name or "collector's" in name) and "chemistry set" in name:
            name = name.replace("collector's", "").replace("chemistry set", "").strip()
            item["defindex"] = 20007 if "festive" in name and "a rather festive tree" not in name else 20006
            schemaItem = self.getItemByItemName(name)
            if not schemaItem: return item
            item["output"] = schemaItem["defindex"]
            item["outputQuality"] = 14
            item["quality"] = item["quality"] or schemaItem["item_quality"] # default quality

        if "strangifier chemistry set" in name:
            name = name.replace("strangifier chemisty set", "").strip()
            schemaItem = self.getItemByItemName(name)
            if not schemaItem: return item
            # Standardize defindex for Strangifier Chemistry Set
            item["defindex"] = 20000
            item["target"] = schemaItem["defindex"]
            item["quality"] = 6
            item["output"] = 6522
            item["outputQuality"] = 6

        if "strangifier" in name:
            name = name.replace("strangifier", "").strip()
            # Standardize to use only 6522
            item["defindex"] = 6522
            schemaItem = self.getItemByItemName(name)
            if not schemaItem: return name
            item["target"] = schemaItem["defindex"]
            item["quality"] = item["quality"] or schemaItem["quality"] # default quality

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
                schemaItem = self.getItemByItemName(name)
                if not schemaItem: return item
                item["target"] = schemaItem["defindex"]
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
                item["defindex"] = self.munitionCratesList.get(str(crateseries))
                item["crateseries"] = crateseries
                item["quality"] = 6
                return item

            number = None

            if "#" in name:
                withoutNumber = name.split('#')[0]
                number = name[len(withoutNumber) + 1:].strip()
                name = name.split('#')[0].strip()

            if name in retiredKeysNames:
                for retiredKey in retiredKeys:
                    if retiredKey['name'].lower() == name:
                        item["defindex"] = retiredKey["defindex"]
                        item["quality"] = item["quality"] or 6
                        return item

            schemaItem = self.getItemByNameWithThe(name)
            if not schemaItem: return item
            item["defindex"] = schemaItem["defindex"]
            item["quality"] = item["quality"] or schemaItem["item_quality"] # default quality

            # Fix defindex for Exclusive Genuine items
            if item["quality"] == 1:
                if item["defindex"] in exclusiveGenuine:
                    item["defindex"] = exclusiveGenuine[item['defindex']]

            if schemaItem["item_class"] == "supply_crate":
                item["crateseries"] = self.getCrateSeriesList()[str(item["defindex"])]
            
            elif schemaItem["item_class"] != "supply_crate" and number is not None:
                item["craftnumber"] = number

        return item


    # Gets schema item by defindex
    def getItemByDefindex(self, defindex):
        items = self.raw["schema"]["items"]
        itemsCount = len(items)
        start = 0
        end = itemsCount - 1
        iterLim = math.ceil(math.log2(itemsCount)) + 2
        while start <= end:
            if iterLim <= 0: break # use fallback search
            iterLim = iterLim - 1
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


    # Gets schema item by item name
    def getItemByItemName(self, name):
        items = self.raw["schema"]["items"]

        for item in items:
            if name.lower() == item["item_name"].lower():
                if item["item_name"] == "Name Tag" and item["defindex"] == 2093:
                    # skip and let it find Name Tag with defindex 5020
                    continue

                if item["item_quality"] == 0:
                    # skip if Stock Quality
                    continue

                return item
        
        return None


    # Gets schema item by sku
    def getItemBySKU(self, sku):
        return self.getItemByDefindex(SKU.fromString(sku)["defindex"])


    # Gets schema attribute by defindex
    def getAttributeByDefindex(self, defindex):
        attributes = self.raw["schema"]["attributes"]
        attributesCount = len(attributes)
        
        start = 0
        end = attributesCount - 1
        iterLim = math.ceil(math.log2(attributesCount)) + 2

        while start <= end:
            if iterLim <= 0: break # use fallback search
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


    # Gets quality name by id
    def getQualityById(self, id):
        qualities = self.raw["schema"]["qualities"]
        
        for type in qualities:
            if type not in qualities: continue

            if qualities[type] == id: return self.raw["schema"]["qualityNames"][type]
        
        return None

    
    # Gets quality id by name
    def getQualityByName(self, name):
        qualityNames = self.raw["schema"]["qualityNames"]
        
        for type in qualityNames:
            if not qualityNames.get(type): continue

            if name.lower() == qualityNames[type].lower(): return self.raw["schema"]["qualities"][type]
        
        return None

    
    # Gets effect name by id
    def getEffectById(self, id):
        particles = self.raw["schema"]["attribute_controlled_attached_particles"]
        particlesCount = len(particles)

        start = 0
        end = particlesCount -1
        iterLim = math.ceil(math.log2(particlesCount)) + 2
        while start <= end:
            if iterLim <= 0: break # use fallback search
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


    # Gets effect id by name
    def getEffectIdByName(self, name):
        particles = self.raw["schema"]["attribute_controlled_attached_particles"]
        
        for effect in particles:
            if name.lower() == effect["name"].lower(): return effect["id"]

        return None


    # Gets skin name by id
    def getSkinById(self, id):
        paintkits = self.raw["schema"]['paintkits']

        if not paintkits.get(str(id)): return None

        return paintkits[str(id)]


    # Gets skin id by name
    def getSkinByName(self, name):
        paintkits = self.raw["schema"]['paintkits']

        for id in paintkits:
            if not paintkits.get(id): continue

            if name.lower() == paintkits[id].lower(): return int(id)

        return None


    # Gets the name and id of unusual effects
    def getUnusualEffects(self):
        unusualEffects = []

        for effect in self.raw["schema"]["attribute_controlled_attached_particles"]:
            unusualEffects.append({"name": effect["name"], "id": effect["id"]})
        
        return unusualEffects


    # Gets paint name by Decimal numeral system
    def getPaintNameByDecimal(self, decimal):
        if decimal == 5801378: return "Legacy Paint"

        paintCans = []
        for item in self.raw["schema"]["items"]:
            if "Paint Can" in item["name"] and item["name"] != "Paint Can":
                paintCans.append(item)

        for paint in paintCans:
            if paint["attributes"] is None: continue

            for attr in paint["attributes"]:
                if attr["value"] == decimal: return paint["item_name"]
        
        return None


    # Gets paint Decimal numeral system by name
    def getPaintDecimalByName(self, name):
        if name == "Legacy Paint": return 5801378

        paintCans = []
        for item in self.raw["schema"]["items"]:
            if "Paint Can" in item["name"] and item["name"] != "Paint Can":
                paintCans.append(item)
        
        for paint in paintCans:
            if paint["attributes"] is None: continue

            if name.lower() == paint["item_name"].lower(): return paint["attributes"][0]["value"]

        return None


    # Gets the name and partial sku for painted items
    def getPaints(self):
        paintCans = []
        for item in self.raw["schema"]["items"]:
            if "Paint Can" in item["name"] and item["name"] != "Paint Can":
                paintCans.append(item)

        toObject = {}
        
        for paintCan in paintCans:
            if paintCan["attributes"] is None: continue

            toObject[paintCan["item_name"]] = f"p{paintCan['attributes'][0]['value']}"

        toObject["Legacy Paint"] = "p5801378"

        return toObject


    # Gets an array of paintable items' defindex
    def getPaintableItemDefindexes(self):
        paintableItemDefindexes = []
        for item in self.raw["schema"]["items"]:
            if "capabilities" in item and "paintable" in item["capabilities"] and item["capabilities"]["paintable"] is True: paintableItemDefindexes.append(item["defindex"])
        return paintableItemDefindexes

    
    # Gets the name of partial sku for strange parts items
    def getStrangeParts(self):
        partsToExclude = {
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

        toObject = {}

        # Filter out built-in parts and also filter repeated "Kills"
        parts = []
        for type in self.raw["schema"]["kill_eater_score_types"]:
            if type["type_name"] not in partsToExclude and type["type"] not in [0, 97]: parts.append(type)

        for part in parts:
            toObject[part["type_name"]] = f"sp{part['type']}"

        return toObject


    # Get an array of item objects for craftable weapons
    def getCraftableWeaponsSchema(self):
        weaponsToExclude = {
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

        craftableWeapons = []
        for item in self.raw["schema"]["items"]:
            if item["defindex"] not in weaponsToExclude and item["item_quality"] == 6 and item.get("craft_class") == "weapon": craftableWeapons.append(item)

        return craftableWeapons


    # Get an array of SKU for craftable weapons by class used for crafting
    def getWeaponsForCraftingByClass(self, charClass):
        if charClass not in {'Scout', 'Soldier', 'Pyro', 'Demoman', 'Heavy', 'Engineer', 'Medic', 'Sniper', 'Spy'}:
            raise Exception(f'Entered class "{charClass}" is not a valid character class.\nValid character classes (case sensitive): "Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy".')
        
        weapons = []
        for item in self.getCraftableWeaponsSchema():
            if charClass in item["used_by_classes"]: weapons.append(f'{item["defindex"]};6')

        return weapons

    
    # Get an array of SKU for Craftable weapons used for trading
    def getCraftableWeaponsForTrading(self):
        weapons = []
        for item in self.getCraftableWeaponsSchema():
            weapons.append(f"{item['defindex']};6")
        [weapons.append(f"{defindex};6") for defindex in [1178, 1179, 1180, 1181, 1190]]
        return weapons


    # Get an array of SKU for Non-Craftable weapons used for trading
    def getUncraftableWeaponsForTrading(self):
        weapons = []
        for item in self.getCraftableWeaponsSchema():
            if item["defindex"] not in [348, 349]: weapons.append(f"{item['defindex']};6;uncraftable")
        return weapons


    def getCrateSeriesList(self):
        items = self.raw["schema"]["items"]

        crateseries = {}
        for item in items:
            if "attributes" in item:
                attributes = item["attributes"]
                for attr in attributes:
                    if attr["name"] == "set supply crate series": 
                        crateseries.update({str(item["defindex"]): int(attr["value"])})
                        break

        items = self.raw["items_game"]["items"]
        defindexes = [x for x in items]

        for defindex in defindexes:
            if items[defindex].get("static_attrs") and items[defindex]["static_attrs"].get("set supply crate series"):
                crateseries.update({str(defindex): int(items[defindex]["static_attrs"]["set supply crate series"])})

        items = None
        return crateseries

    
    def updateCrateSeriesList(self):
        self.crateSeriesList = self.getCrateSeriesList


    def checkExistence(self, item):
        schemaItem = self.getItemByDefindex(item["defindex"])
        if not schemaItem: return False

        # Items with default quality
        if schemaItem["item_quality"] in {0, 3, 5, 11}:
            # default Normal (Stock items), Vintage (1156), Unusual (266, 267), and Strange (655) items
            if item.get("quality") != schemaItem["item_quality"]: return False

        # Exclusive Genuine items
        if ((item.get("quality") != 1 and item["defindex"] in [exclusiveGenuineReversed.get(egr) for egr in exclusiveGenuineReversed]) or 
            (item.get("quality") == 1 and item["defindex"] in [exclusiveGenuine.get(eg) for eg in exclusiveGenuine])):
            # if quality not 1 AND item.defindex is the one that should be Genuine only, OR
            # if quality is 1 AND item.defindex is the one that can be any quality, return null.
            return False

        # Retired keys
        for retiredKey in retiredKeys:
            if retiredKey.get("defindex") == item["defindex"]:
                if item["defindex"] in [5713, 5716, 5717, 5762]:
                    if item.get("craftable") is True:
                        return False
                elif item["defindex"] not in [5791, 5792]:
                    if item.get("craftable") is False:
                        return False

        # Crates/Cases
        def haveOtherAttributeForCrateOrCase():
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
        if schemaItem["item_class"] == "supply_crate" and item.get("crateseries") is None:
            if item["defindex"] not in {5739, 5760, 5737, 5738}:
                # If not seriesless, return false
                # Mann Co. Director's Cut Reel, Mann Co. Audition Reel, and Mann Co. Stockpile Crate
                return False
            # Unlocked Creepy 5763, 5764, 5765, 5766, 5767, 5768, 5769, 5770, 5771
            # Unlocked Crates 5850, 5851, 5852, 5853, 5854, 5855, 5856, 5857, 5858, 5860
            if haveOtherAttributeForCrateOrCase(): return False
        if item.get("crateseries"):
            # Run a check if the input item is actually exist or not for crates/cases
            if haveOtherAttributeForCrateOrCase(): return False
            if schemaItem["item_class"] != "supply_crate":
                # Not a crate or case
                return False
            elif (item["crateseries"] not in {1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75, 2, 4, 8, 11, 14, 17, 20, 24, 27,
                32, 37, 42, 44, 49, 56, 71, 76, 5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77, 30,
                40, 50, 82, 83, 84, 85, 90, 91, 92, 103}):
                # if item["crateseries"] not included in the single defindex multiple series crate:
                if item["crateseries"] not in [self.crateSeriesList[cratesSeries] for cratesSeries in self.crateSeriesList]:
                    # if item["crateseries"] is not included in the crateSeriesList, does not exist.
                    return False
                # Check for specific crates/cases
                if item["crateseries"] != self.crateSeriesList[item["defindex"]]: return False
            elif not (
                (item["crateseries"] in {1, 3, 7, 12, 13, 18, 19, 23, 26, 31, 34, 39, 43, 47, 54, 57, 75} and item["defindex"] == 5022) or
                (item["crateseries"] in {2, 4, 8, 11, 14, 17, 20, 24, 27, 32, 37, 42, 44, 49, 56, 71, 76} and item["defindex"] == 5041) or
                (item["crateseries"] in {5, 9, 10, 15, 16, 21, 25, 28, 29, 33, 38, 41, 45, 55, 59, 77} and item["defindex"] == 5045) or
                (item["crateseries"] in {30, 40, 50} and item["defindex"] == 5068) or
                (self.munitionCratesList.get(str(item["crateseries"])) and item["defindex"] == self.munitionCratesList.get(str(item["crateseries"])))):
                # if single defindex multiple series crate don't match, does not exist
                return False

        return True


    # Gets the name of an item with specific attributes
    def getName(self, item, proper=True, usePipeForSkin=False):
        schemaItem = self.getItemByDefindex(item["defindex"])
        if schemaItem is None: return None

        name = ""

        if item.get("tradable") is False: name = "Non-Tradable "

        if item.get("craftable") is False: name += "Non-Craftable "

        if item.get("quality2"):
            # Elevated quality
            name += self.getQualityById(item["quality2"]) + " "

        if ((item["quality"] != 6 and item["quality"] != 15 and item["quality"]  != 5) or
            (item["quality"]  == 5 and not item.get("effect")) or
            (item["quality"] == 6 and item.get("quality2")) or
            schemaItem["item_quality"] == 5):
            # If the quality is Unique (and is Elevated quality) or not Unique, Decorated, or Unusual, or if the quality is Unusual but it does not have an effect, or if the item can only be unusual, then add the quality
            name += self.getQualityById(item["quality"]) + " "

        if item.get("effect"): name += self.getEffectById(item["effect"]) + " "

        if item.get("festive") is True: name += "Festivized "

        if item.get("killstreak") and item["killstreak"] > 0: name += ['Killstreak', 'Specialized Killstreak', 'Professional Killstreak'][item["killstreak"] - 1] + ' '

        if item.get("target"): name += self.getItemByDefindex(item["target"])["item_name"] + " "

        if item.get("outputQuality") and item["outputQuality"] != 6: name = self.getQualityById(item["outputQuality"]) + " " + name

        if item.get("output"): name += self.getItemByDefindex(item["output"])["item_name"] + " "

        if item.get("australium") is True: name += "Australium "

        if item.get("paintkit") and type(item["paintkit"]) == int: name += self.getSkinById(item["paintkit"]) + (" " if usePipeForSkin is False else " | ")

        if proper is True and name == "" and schemaItem["proper_name"] is True: name = "The "

        for retiredKey in retiredKeys:
            if retiredKey.get("defindex") == item["defindex"]:
                name += retiredKey["name"]
                break
        else:
            name += schemaItem["item_name"]

        if item.get("wear"): name += ' (' + ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle Scarred'][item["wear"] - 1] + ')'

        if item.get("crateseries"): name += " #" + str(item["crateseries"])
        
        if item.get("craftnumber"): name += ' #' + str(item["craftnumber"])

        if item.get("paint"): name += f" (Paint: {self.getPaintNameByDecimal(item['paint'])})"

        return name


    # Gets name
    def getNameFromSku(self, sku):
        if self.testSKU(sku) is True:
            return self.getName(SKU.fromString(sku))
        else:
            return None

    
    # Check sku if it's valid or not
    def testSKU(self, sku):
        if bool(re.match(
            "^(\d+);([0-9]|[1][0-5])(;((uncraftable)|(untrad(e)?able)|(australium)|(festive)|(strange)|((u|pk|td-|c|od-|oq-|p)\d+)|(w[1-5])|(kt-[1-3])|(n((100)|[1-9]\d?))))*?$", sku)):
            return True

    
    # Gets munition crate list
    def getMunitionCratesList(self):
        munitionCratesList = {}
        items = self.raw["schema"]["items"]
        for item in items:
            if item["item_name"] == "Mann Co. Supply Munition":
                munitionCratesList.update({str(item["attributes"][0]["value"]): int(item["defindex"])})
        return munitionCratesList


    # Gets weapon skins list
    def getWeaponSkinsList(self):
        items = self.raw["items_game"]["items"]
        pistolSkins = {}
        rocketLauncherSkins = {}
        medicgunSkins = {}
        revolverSkins = {}
        stickybombSkins = {}
        sniperRifleSkins = {}
        flameThrowerSkins = {}
        minigunSkins = {}
        scattergunSkins = {}
        shotgunSkins = {}
        smgSkins = {}
        wrenchSkins = {}
        grenadeLauncherSkins = {}
        knifeSkins = {}
        for item in items:
            if items[item].get("prefab"):
                if items[item]["prefab"] == "paintkit_weapon_pistol":
                    pistolSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_rocketlauncher":
                    rocketLauncherSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_medigun":
                    medicgunSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_revolver":
                    revolverSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_stickybomb_launcher":
                    stickybombSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_sniperrifle":
                    sniperRifleSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_flamethrower":
                    flameThrowerSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_minigun":
                    minigunSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_scattergun":
                    scattergunSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_shotgun":
                    shotgunSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_smg":
                    smgSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_wrench":
                    wrenchSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_grenadelauncher":
                    grenadeLauncherSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
                elif items[item]["prefab"] == "paintkit_weapon_knife":
                    knifeSkins.update({str(items[item]["static_attrs"]["paintkit_proto_def_index"]): int(item)})
        weaponSkinsList = {
            "pistolSkins": pistolSkins,
            "rocketLauncherSkins": rocketLauncherSkins,
            "medicgunSkins": medicgunSkins,
            "revolverSkins": revolverSkins,
            "stickybombSkins": stickybombSkins,
            "sniperRifleSkins": sniperRifleSkins,
            "flameThrowerSkins": flameThrowerSkins,
            "minigunSkins": minigunSkins,
            "scattergunSkins": scattergunSkins,
            "shotgunSkins": shotgunSkins,
            "smgSkins": smgSkins,
            "wrenchSkins": wrenchSkins,
            "grenadeLauncherSkins": grenadeLauncherSkins,
            "knifeSkins": knifeSkins
        }
        return weaponSkinsList


    # Gets schema overview
    @staticmethod
    def getOverview(apiKey):
        input = {
            "key": apiKey,
            "language": "en"
        }
        overview = WebRequest('GET', 'GetSchemaOverview', 'v0001', input)["result"]
        del overview["status"]
        return overview


    # Gets schema items
    @staticmethod
    def getItems(apiKey):
        return getAllSchemaItems(apiKey)


    # Gets skins / paintkits from TF2 protodefs
    @staticmethod
    def getPaintKits():
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
            paintkitsObj = {}
            for paintKit in paintkits:
                paintKitName = paintKit["name"]
                if paintKitName not in [paintkitsObj[paintkit] for paintkit in paintkitsObj]:
                    paintkitsObj[paintKit["id"]] = paintKit["name"]
            return paintkitsObj
        else:
            raise Exception("Failed to get paintkits.")


    @staticmethod
    def getItemsGame():
        response = requests.get('https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/scripts/items/items_game.txt', timeout=10)
        if response.status_code == 200:
            return vdf.loads(response.text)["items_game"]
        else:
            raise Exception("Failed to get items game.")


# Recursive function that requests all schema items
def getAllSchemaItems(apiKey):
    input = {
        "key": apiKey,
        "language": "en"
    }
    result = WebRequest('GET', 'GetSchemaItems', 'v0001', input)
    items = result["result"]["items"]
    while "next" in result["result"]:
        input = {
            "key": apiKey,
            "language": "en",
            "start": result["result"]["next"]
        }
        result = WebRequest('GET', 'GetSchemaItems', 'v0001', input)
        items = items + result["result"]["items"]
    return items
