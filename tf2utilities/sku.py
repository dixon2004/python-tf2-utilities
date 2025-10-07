# Constants for attribute defindexes (for fast lookups)
ATTR_KILLSTREAK = 2025
ATTR_AUSTRALIUM = 2027
ATTR_EFFECT = 134
ATTR_FESTIVE = 2053
ATTR_PAINTKIT = 834
ATTR_WEAR = 749
ATTR_QUALITY2 = 214
ATTR_CRAFTNUMBER = 229
ATTR_CRATESERIES = 187
ATTR_TARGET = 2012
ATTR_PAINT = 142

# Template for item objects (shared to reduce allocations)
ITEM_TEMPLATE = {
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


class SKU:
    # Convert SKU to item object (optimized)
    @staticmethod
    def fromString(sku):
        result = ITEM_TEMPLATE.copy()

        parts = sku.split(";")

        # Parse defindex (first part)
        if parts and parts[0].isnumeric():
            result["defindex"] = int(parts[0])
            parts = parts[1:]

        # Parse quality (second part)
        if parts and parts[0].isnumeric():
            result["quality"] = int(parts[0])
            parts = parts[1:]

        # Parse remaining attributes
        for part in parts:
            part_stripped = part.replace("-", "")

            # Simple string flags
            if part_stripped == "uncraftable":
                result["craftable"] = False
            elif part_stripped in ("untradeable", "untradable"):
                result["tradable"] = False
            elif part_stripped == "australium":
                result["australium"] = True
            elif part_stripped == "festive":
                result["festive"] = True
            elif part_stripped == "strange":
                result["quality2"] = 11
            # Prefixed numeric attributes
            elif len(part_stripped) > 2:
                prefix = part_stripped[:2]
                suffix = part_stripped[2:]
                if suffix.isnumeric():
                    value = int(suffix)
                    if prefix == "kt":
                        result["killstreak"] = value
                    elif prefix == "pk":
                        result["paintkit"] = value
                    elif prefix == "td":
                        result["target"] = value
                    elif prefix == "od":
                        result["output"] = value
                    elif prefix == "oq":
                        result["outputQuality"] = value
            # Single-char prefix attributes
            if len(part_stripped) > 1:
                prefix = part_stripped[0]
                suffix = part_stripped[1:]
                if suffix.isnumeric():
                    value = int(suffix)
                    if prefix == "u":
                        result["effect"] = value
                    elif prefix == "w":
                        result["wear"] = value
                    elif prefix == "n":
                        result["craftnumber"] = value
                    elif prefix == "c":
                        result["crateseries"] = value
                    elif prefix == "p":
                        result["paint"] = value

        return result


    # Convert item object to SKU (optimized)
    @staticmethod
    def fromObject(item):
        # Use list for faster string building
        parts = [str(item.get("defindex", 0)), str(item.get("quality", 0))]

        # Append parts in order for consistent SKU format
        if item.get("effect"):
            parts.append(f"u{item['effect']}")
        if item.get("australium") is True:
            parts.append("australium")
        if item.get("craftable") is False:
            parts.append("uncraftable")
        if item.get("tradable") is False:
            parts.append("untradable")
        if item.get("wear"):
            parts.append(f"w{item['wear']}")
        if item.get("paintkit") and isinstance(item['paintkit'], int):
            parts.append(f"pk{item['paintkit']}")
        if item.get("quality2") == 11:
            parts.append("strange")

        killstreak = item.get("killstreak")
        if killstreak and isinstance(killstreak, int) and killstreak != 0:
            parts.append(f"kt-{killstreak}")

        if item.get("target"):
            parts.append(f"td-{item['target']}")
        if item.get("festive") is True:
            parts.append("festive")
        if item.get("craftnumber"):
            parts.append(f"n{item['craftnumber']}")
        if item.get("crateseries"):
            parts.append(f"c{item['crateseries']}")
        if item.get("output"):
            parts.append(f"od-{item['output']}")
        if item.get("outputQuality"):
            parts.append(f"oq{item['outputQuality']}")
        if item.get("paint"):
            parts.append(f"p{item['paint']}")

        return ";".join(parts)

    
    @staticmethod
    def fromAPI(item):
        """Convert API item to SKU (optimized with attribute lookup table)"""
        result = ITEM_TEMPLATE.copy()

        result["defindex"] = item["defindex"]
        result["quality"] = item["quality"]

        if item.get("flag_cannot_craft"):
            result["craftable"] = False
        if item.get("flag_cannot_trade"):
            result["tradable"] = False

        attributes = item.get("attributes")
        if attributes:
            item_quality = item['quality']

            for attribute in attributes:
                # Convert defindex once per iteration
                attr_defindex = int(attribute["defindex"])

                # Use dictionary lookup for faster attribute processing
                if attr_defindex == ATTR_KILLSTREAK:
                    result["killstreak"] = attribute["float_value"]
                elif attr_defindex == ATTR_AUSTRALIUM:
                    result["australium"] = attribute['float_value'] == 1
                elif attr_defindex == ATTR_EFFECT:
                    result["effect"] = attribute['float_value']
                elif attr_defindex == ATTR_FESTIVE:
                    result["festive"] = attribute['float_value'] == 1
                elif attr_defindex == ATTR_PAINTKIT:
                    result["paintkit"] = attribute["float_value"]
                elif attr_defindex == ATTR_WEAR:
                    result["wear"] = attribute["float_value"]
                elif attr_defindex == ATTR_QUALITY2 and item_quality == 5:
                    result["quality2"] = attribute["value"]
                elif attr_defindex == ATTR_CRAFTNUMBER:
                    result["craftnumber"] = attribute["value"]
                elif attr_defindex == ATTR_CRATESERIES:
                    result["crateseries"] = attribute["float_value"]
                elif attr_defindex == ATTR_PAINT:
                    result["paint"] = attribute["float_value"]
                elif 2000 <= attr_defindex <= 2009:
                    # Handle nested attributes for target
                    nested_attrs = attribute.get("attributes")
                    if nested_attrs:
                        for attr in nested_attrs:
                            if int(attr["defindex"]) == ATTR_TARGET:
                                result["target"] = attr["float_value"]
                                break

                # Handle output items
                if attribute.get("is_output") is True:
                    result["output"] = attribute["itemdef"]
                    result["outputQuality"] = attribute["quantity"]

        return SKU.fromObject(result)
