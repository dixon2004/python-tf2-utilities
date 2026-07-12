import re
from typing import Optional

LEGACY_PAINT_ICON = "SLcfMQEs5nqWSMU5OD2NwHzHZdmi"


class SKU:

    @staticmethod
    def from_string(sku: str) -> dict:
        """
        Converts a SKU to an item object.
        
        Args:
            sku (str): The SKU to convert.
            
        Returns:
            dict: The item object.
        """
        TEMPLATE = {
            "defindex": 0,
            "quality": 0,
            "craftable": True,
            "tradable": True,
            "killstreak": 0,
            "australium": False,
            "effect": None,
            "festive": False,
            "paintkit": None,
            "wear": None,
            "quality2": None,
            "craftnumber": None,
            "crateseries": None,
            "target": None,
            "output": None,
            "outputQuality": None,
            "paint": None
        }
        attributes = {}
        
        parts = sku.split(";")
        parts_count = len(parts)

        if parts_count > 0:
            if str(parts[0]).isnumeric():
                attributes["defindex"] = int(parts[0])
            parts.pop(0)

        if parts_count > 0:
            if str(parts[0]).isnumeric():
                attributes["quality"] = int(parts[0])
            parts.pop(0)

        for part in parts:
            attribute = str(part.replace("-", ""))

            if attribute == "uncraftable":
                attributes["craftable"] = False
            elif attribute in ["untradeable", "untradable"]:
                attributes["tradable"] = False
            elif attribute == "australium":
                attributes["australium"] = True
            elif attribute == "festive":
                attributes["festive"] = True
            elif attribute == "strange":
                attributes["quality2"] = 11
            elif attribute.startswith("kt") and attribute[2:].isnumeric():
                attributes["killstreak"] = int(attribute[2:])
            elif attribute.startswith("u") and attribute[1:].isnumeric():
                attributes["effect"] = int(attribute[1:])
            elif attribute.startswith("pk") and attribute[2:].isnumeric():
                attributes["paintkit"] = int(attribute[2:])
            elif attribute.startswith("w") and attribute[1:].isnumeric():
                attributes["wear"] = int(attribute[1:])
            elif attribute.startswith("td") and attribute[2:].isnumeric():
                attributes["target"] = int(attribute[2:])
            elif attribute.startswith("n") and attribute[1:].isnumeric():
                attributes["craftnumber"] = int(attribute[1:])
            elif attribute.startswith("c") and attribute[1:].isnumeric():
                attributes["crateseries"] = int(attribute[1:])
            elif attribute.startswith("od") and attribute[2:].isnumeric():
                attributes["output"] = int(attribute[2:])
            elif attribute.startswith("oq") and attribute[2:].isnumeric():
                attributes["outputQuality"] = int(attribute[2:])
            elif attribute.startswith("p") and attribute[1:].isnumeric():
                attributes["paint"] = int(attribute[1:])

        for attr in TEMPLATE:
            if attr in attributes: TEMPLATE[attr] = attributes[attr]

        return TEMPLATE


    @staticmethod
    def from_object(item: dict) -> str:
        """
        Converts an item object to a SKU.
        
        Args:
            item (dict): The item object to convert.
            
        Returns:
            str: The SKU.
        """
        TEMPLATE = {
            "defindex": 0,
            "quality": 0,
            "craftable": True,
            "tradable": True,
            "killstreak": 0,
            "australium": False,
            "effect": None,
            "festive": False,
            "paintkit": None,
            "wear": None,
            "quality2": None,
            "craftnumber": None,
            "crateseries": None,
            "target": None,
            "output": None,
            "outputQuality": None,
            "paint": None
        }
        for attr in TEMPLATE:
            if attr in item: TEMPLATE[attr] = item[attr]

        sku = f'{item["defindex"]};{item["quality"]}'

        if item.get("effect"): sku += f";u{item['effect']}"
        if item.get("australium") is True: sku += ";australium"
        if item.get("craftable") is False: sku += ";uncraftable"
        if item.get("tradable") is False: sku += ";untradable"
        if item.get("wear"): sku += f";w{item['wear']}"
        if item.get("paintkit") is not None and isinstance(item['paintkit'], int): sku += f";pk{item['paintkit']}"
        if item.get("quality2") and item["quality2"] == 11: sku += ";strange"
        if item.get("killstreak") and isinstance(item['killstreak'], int) and item["killstreak"] != 0: sku += f";kt-{item['killstreak']}"
        if item.get("target"): sku += f";td-{item['target']}"
        if item.get("festive") is True: sku += ';festive'
        if item.get("craftnumber"): sku += f";n{item['craftnumber']}"
        if item.get("crateseries"): sku += f";c{item['crateseries']}"
        if item.get("output"): sku += f";od-{item['output']}"
        if item.get("outputQuality"): sku += f";oq-{item['outputQuality']}"
        if item.get("paint"): sku += f";p{item['paint']}"
        
        return sku

    
    @staticmethod
    def from_API(item: dict, schema) -> str:
        """
        Converts a Steam Community inventory item description into a SKU.

        Args:
            item (dict): An item description object from the inventory endpoint.
            schema: A tf2utilities Schema instance, used for name/quality/effect/skin/paint
                lookups and Strangifier target resolution.

        Returns:
            str: The SKU.
        """
        if not item.get("market_hash_name"):
            raise ValueError('Item does not have the "market_hash_name" key, unable to identify the item')

        defindex = _api_defindex(item)
        quality = _api_quality(item, schema)
        killstreak = _api_killstreak(item)
        wear = _api_wear(item)

        parsed = _api_parse_descriptions(item, schema, defindex, wear, killstreak)
        crateseries = _api_crate_series(item, defindex)

        sku_obj = {
            "defindex": defindex,
            "quality": quality,
            "craftable": parsed["craftable"],
            "tradable": bool(item.get("tradable")),
            "killstreak": killstreak,
            "australium": _api_is_australium(item, quality),
            "effect": parsed["effect"],
            "festive": "Festivized " in item["market_hash_name"],
            "paintkit": parsed["paintkit"],
            "wear": wear,
            "quality2": None,
            "craftnumber": _api_craft_number(item, schema, defindex, crateseries),
            "crateseries": crateseries,
            "target": parsed["target"],
            "output": parsed["output"],
            "outputQuality": parsed["outputQuality"],
            "paint": parsed["paint"],
        }

        elevated_quality = _api_elevated_quality(item, parsed["paintkit"], quality, parsed["hasStatClock"])
        if isinstance(elevated_quality, dict):
            sku_obj["quality2"] = elevated_quality["elevatedQuality"]
            sku_obj["quality"] = elevated_quality["replaceQuality"]
        else:
            sku_obj["quality2"] = elevated_quality

        if sku_obj["target"] is None:
            sku_obj["target"] = _api_target(item, schema, defindex)

        if crateseries is None:
            sku_obj = schema.fix_item(sku_obj)

        item_sku = SKU.from_object(sku_obj)
        if "none" in item_sku.lower():
            raise Exception(f'Item SKU is invalid for "{item.get("market_hash_name")}"')

        return item_sku


def _api_get_action(item: dict, action: str) -> Optional[str]:
    """
    Returns the link for the named action on an inventory item, or None.
    
    Args:
        item (dict): An item description object from the inventory endpoint.
        action (str): The name of the action to look for.

    Returns:
        Optional[str]: The link for the action, or None if not found.
    """
    actions = item.get("actions")
    if not isinstance(actions, list):
        return None
    for a in actions:
        if isinstance(a, dict) and a.get("name") == action and "link" in a:
            return a["link"]
    return None


def _api_get_tag(item: dict, category: str) -> Optional[str]:
    """
    Returns the localized tag value for the given tag category, or None.

    Args:
        item (dict): An item description object from the inventory endpoint.
        category (str): The category of the tag to look for.

    Returns:
        Optional[str]: The localized tag value, or None if not found.
    """
    tags = item.get("tags")
    if not isinstance(tags, list):
        return None
    for tag in tags:
        if isinstance(tag, dict) and tag.get("category") == category:
            return tag.get("localized_tag_name") or tag.get("name")
    return None


def _api_safe_defindex(schema, name: str) -> Optional[int]:
    """
    Returns the defindex of the schema item with the given name, or None if not found.

    Args:
        schema: A tf2utilities Schema instance.
        name (str): The market hash name of the item.

    Returns:
        Optional[int]: The defindex of the item, or None if not found.
    """
    schema_item = schema.get_item_by_item_name(name)
    return schema_item["defindex"] if schema_item else None


def _api_defindex(item: dict) -> int:
    """
    Extracts the item's defindex from its "Item Wiki Page..." action link (0 if absent).

    Args:
        item (dict): An item description object from the inventory endpoint.

    Returns:
        int: The defindex of the item, or 0 if not found.
    """
    link = _api_get_action(item, "Item Wiki Page...")
    if link:
        match = re.search(r"id=(\d+)", link)
        if match:
            return int(match.group(1))
    return 0


def _api_quality(item: dict, schema) -> Optional[int]:
    """
    Returns the quality id from the item's Quality tag, or None if the tag is absent.

    Args:
        item (dict): An item description object from the inventory endpoint.
        schema: A tf2utilities Schema instance.

    Returns:
        Optional[int]: The quality id, or None if the tag is absent.
    """
    quality_from_tag = _api_get_tag(item, "Quality")
    if quality_from_tag:
        return schema.get_quality_by_name(quality_from_tag)
    return None


def _api_killstreak(item: dict) -> int:
    """
    Returns the killstreak tier (0=none, 1=basic, 2=specialized, 3=professional).

    Args:
        item (dict): An item description object from the inventory endpoint.

    Returns:
        int: The killstreak tier.
    """
    for index, killstreak in enumerate(["Professional ", "Specialized ", ""]):
        if killstreak + "Killstreak " in item["market_hash_name"]:
            return 3 - index
    return 0


def _api_wear(item: dict) -> Optional[int]:
    """
    Returns the wear tier (1=Factory New .. 5=Battle Scarred) from the Exterior tag, or None.

    Args:
        item (dict): An item description object from the inventory endpoint.

    Returns:
        Optional[int]: The wear tier, or None if the tag is absent.
    """
    wears = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle Scarred"]
    exterior = _api_get_tag(item, "Exterior")
    if exterior in wears:
        return wears.index(exterior) + 1
    return None


def _api_is_australium(item: dict, quality: Optional[int]) -> bool:
    """
    Returns True if the item is an Australium (Strange-quality) weapon.

    Args:
        item (dict): An item description object from the inventory endpoint.
        quality (Optional[int]): The quality id of the item.

    Returns:
        bool: True if the item is an Australium, False otherwise.
    """
    if quality != 11:
        return False
    return "Australium " in item["market_hash_name"]


def _api_elevated_quality(item: dict, paintkit: Optional[int], quality: Optional[int], has_stat_clock: bool):
    """
    Resolves an item's elevated (secondary) quality.

    Args:
        item (dict): An item description object from the inventory endpoint.
        paintkit (Optional[int]): The paintkit id of the item.
        quality (Optional[int]): The quality id of the item.
        has_stat_clock (bool): True if the item has a Strange Stat Clock attached, False otherwise.

    Returns:
        Plain elevated-Strange items return 11 (int). Strange war paints/skins return a
        {"elevatedQuality", "replaceQuality"} dict overriding both quality fields. Items
        with no elevated quality return None.
    """
    item_type = item.get("type") or ""
    is_unusual_hat = (
        _api_get_tag(item, "Type") == "Cosmetic" and quality == 5
        and "Strange" in item_type and "Points Scored" in item_type
    )
    is_other_items_not_strange_quality = item_type.startswith("Strange") and quality != 11

    if has_stat_clock or is_unusual_hat or is_other_items_not_strange_quality:
        if isinstance(paintkit, int):
            tags = item.get("tags") or []
            has_rarity_grade_tag = any(
                isinstance(t, dict) and t.get("category") == "Rarity" and t.get("category_name") == "Grade"
                for t in tags
            )
            has_war_paint_type_tag = _api_get_tag(item, "Type") == "War Paint"
            if has_war_paint_type_tag or not has_rarity_grade_tag:
                return {"elevatedQuality": None, "replaceQuality": 11}
            elif has_rarity_grade_tag and quality == 11:
                return {"elevatedQuality": 11, "replaceQuality": 15}
        return 11
    return None


def _api_target(item: dict, schema, defindex: int) -> Optional[int]:
    """
    Resolves the target item's defindex for Strangifiers, Killstreak Kits and Unusualifiers.

    Args:
        item (dict): An item description object from the inventory endpoint.
        schema: A tf2utilities Schema instance.
        defindex (int): The defindex of the item.

    Returns:
        Optional[int]: The defindex of the target item, or None if not found.
    """
    name = item["market_hash_name"]
    if defindex == 0:
        raise ValueError(f'Could not get defindex of item "{name}"')

    if "Strangifier" in name:
        target = schema.tool_target_list.get(str(defindex))
        if target is not None:
            return target
        schema_item = schema.get_item_by_item_name(name.replace("Strangifier", "", 1).strip())
        if schema_item is not None:
            return schema_item["defindex"]
        raise ValueError(f'Could not find target for item "{name}"')

    length = len(name)
    killstreak_kit_defindexes = {
        6527, 5726, 5727, 5728, 5729, 5730, 5731, 5732, 5733, 5743, 5744, 5745, 5746, 5747, 5748,
        5749, 5750, 5751, 5793, 5794, 5795, 5796, 5797, 5798, 5799, 5800, 5801,
    }
    if defindex in killstreak_kit_defindexes:
        return _api_safe_defindex(schema, name[10:length - 3].replace("Killstreak", "", 1).strip())
    elif defindex == 6523:
        return _api_safe_defindex(schema, name[22:length - 3].strip())
    elif defindex == 6526:
        return _api_safe_defindex(schema, name[23:length - 3].strip())
    elif defindex == 9258:
        return _api_safe_defindex(schema, name[7:length - 12].strip())
    return None


def _api_crate_series(item: dict, defindex: int) -> Optional[int]:
    """
    Returns the series number for multi-series Mann Co. Supply Crates, or None.

    Args:
        item (dict): An item description object from the inventory endpoint.
        defindex (int): The defindex of the item.

    Returns:
        Optional[int]: The series number, or None if the item is not a multi-series crate.
    """
    name = item["market_hash_name"]
    if "Mann Co. Supply Crate Series #" not in name:
        return None
    if defindex not in [5022, 5041, 5045, 5068]:
        return None
    return int(name.replace("Salvaged ", "").replace("Mann Co. Supply Crate Series #", ""))


def _api_craft_number(item: dict, schema, defindex: int, crate_series: Optional[int]) -> Optional[int]:
    """
    Returns the craft number parsed from the item name, or None (skips crates and medals).

    Args:
        item (dict): An item description object from the inventory endpoint.
        schema: A tf2utilities Schema instance.
        defindex (int): The defindex of the item.
        crate_series (Optional[int]): The series number of the crate, or None.

    Returns:
        Optional[int]: The craft number, or None if the item is not a craftable item.
    """
    if crate_series:
        return None
    schema_item = schema.get_item_by_defindex(defindex)
    if schema_item is None or schema_item.get("item_class") == "supply_crate":
        return None
    if defindex == 121:
        # Ignore Gentle Manne's Service Medal: craft number (229) != medal number (133)
        return None
    name = item.get("name", "")
    without_number = re.sub(r"#\d+", "", name, count=1)
    if name == without_number:
        return None
    number = name[len(without_number) + 1:].strip()
    return int(number) if number.isdigit() else None


def _api_parse_descriptions(item: dict, schema, defindex: int, wear: Optional[int], killstreak: int) -> dict:
    """
    Walks the item's descriptions once and extracts craftable, effect, paintkit, target,
    output, outputQuality, paint and hasStatClock.

    Args:
        item (dict): An item description object from the inventory endpoint.
        schema: A tf2utilities Schema instance.
        defindex (int): The item's defindex.
        wear (Optional[int]): The item's wear tier, or None.
        killstreak (int): The item's killstreak tier.

    Returns:
        dict: The parsed description fields.
    """
    parsed = {
        "craftable": True,
        "effect": None,
        "paintkit": None,
        "target": None,
        "output": None,
        "outputQuality": None,
        "paint": None,
        "hasStatClock": False,
    }
    descriptions = item.get("descriptions")
    if not isinstance(descriptions, list):
        return parsed

    contains_case_global = False
    found_unusual = False
    has_case_collection = False
    found_skin = False
    found_uncraftable = False
    found_paint = False
    skin = None
    output_index = -1

    for index, desc in enumerate(descriptions):
        value = desc.get("value", "")

        if not found_uncraftable and value == "( Not Usable in Crafting )":
            found_uncraftable = True
            parsed["craftable"] = False
            continue

        if not parsed["hasStatClock"] and value == "Strange Stat Clock Attached":
            parsed["hasStatClock"] = True
            continue

        if not contains_case_global and value == "Case Global Unusual Effect(s)":
            contains_case_global = True
            continue

        if not found_unusual and not contains_case_global and value.startswith("★ Unusual Effect: "):
            found_unusual = True
            parsed["effect"] = schema.get_effect_id_by_name(value[18:])
            continue

        if not found_skin and wear is not None:
            if not has_case_collection and value.endswith("Collection"):
                has_case_collection = True
                continue
            elif has_case_collection and (value.startswith("✔") or value.startswith("★")):
                found_skin = True
                skin = value[1:].replace(" War Paint", "", 1).strip()
                continue

        if value == "You will receive all of the following outputs once all of the inputs are fulfilled.":
            output_index = index
            continue

        if not found_paint and value.startswith("Paint Color: ") and desc.get("color") == "756b5e":
            found_paint = True
            parsed["paint"] = schema.get_paint_decimal_by_name(value.replace("Paint Color: ", "").strip())
            continue

    if skin is None:
        if has_case_collection and "Red Rock Roscoe Pistol" in item["market_hash_name"]:
            parsed["paintkit"] = 0
    elif found_skin:
        schema_item = schema.get_item_by_defindex(defindex)
        if "Mk.I" in skin or schema_item is None:
            parsed["paintkit"] = schema.get_skin_by_name(skin)
        else:
            parsed["paintkit"] = schema.get_skin_by_name(skin.replace(schema_item.get("item_type_name", ""), "").strip())

    if output_index != -1 and output_index + 1 < len(descriptions):
        output = descriptions[output_index + 1].get("value", "")
        if killstreak != 0:
            prefix = ["Killstreak", "Specialized Killstreak", "Professional Killstreak"][killstreak - 1]
            name = output.replace(prefix, "", 1).replace("Kit", "", 1).strip()
            parsed["target"] = _api_safe_defindex(schema, name)
            parsed["outputQuality"] = 6
            parsed["output"] = [6527, 6523, 6526][killstreak - 1]
        elif " Strangifier" in output:
            name = output.replace("Strangifier", "", 1).strip()
            parsed["target"] = _api_safe_defindex(schema, name)
            parsed["outputQuality"] = 6
            parsed["output"] = 6522
        elif "Collector's" in output:
            name = output.replace("Collector's", "", 1).strip()
            parsed["outputQuality"] = 14
            parsed["output"] = _api_safe_defindex(schema, name)

    if not found_paint and "Tool" not in (item.get("type") or "") and LEGACY_PAINT_ICON in (item.get("icon_url") or ""):
        parsed["paint"] = 5801378

    return parsed
