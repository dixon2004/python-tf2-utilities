class SKU:
    # Convert SKU to item object
    @staticmethod
    def fromString(sku):
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
        partsCount = len(parts)

        if partsCount > 0:
            if str(parts[0]).isnumeric():
                attributes["defindex"] = int(parts[0])
            parts.pop(0)

        if partsCount > 0:
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


    # Convert item object to SKU
    @staticmethod
    def fromObject(item):
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
        if item.get("paintkit") and isinstance(item['paintkit'], int): sku += f";pk{item['paintkit']}"
        if item.get("quality2") and item["quality2"] == 11: sku += ";strange"
        if item.get("killstreak") and isinstance(item['killstreak'], int) and item["killstreak"] != 0: sku += f";kt-{item['killstreak']}"
        if item.get("target"): sku += f";td-{item['target']}"
        if item.get("festive") is True: sku += ';festive'
        if item.get("craftnumber"): sku += f";n{item['craftnumber']}"
        if item.get("crateseries"): sku += f";c{item['crateseries']}"
        if item.get("output"): sku += f";od-{item['output']}"
        if item.get("outputQuality"): sku += f";oq{item['outputQuality']}"
        if item.get("paint"): sku += f";p{item['paint']}"
        
        return sku

    
    @staticmethod
    def fromAPI(item):
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

        TEMPLATE["defindex"] = item["defindex"]
        TEMPLATE["quality"] = item["quality"]
        if item.get("flag_cannot_craft"): TEMPLATE["craftable"] = False
        if item.get("flag_cannot_trade"): TEMPLATE["tradable"] = False
        if item.get("attributes"):
            for attribute in item["attributes"]:
                if int(attribute["defindex"]) == 2025: TEMPLATE["killstreak"] = attribute["float_value"]
                if int(attribute["defindex"])  == 2027: TEMPLATE["australium"] = True if attribute['float_value'] == 1 else False
                if int(attribute["defindex"]) == 134: TEMPLATE["effect"] = attribute['float_value']
                if int(attribute["defindex"]) == 2053: TEMPLATE["festive"] = True if attribute['float_value'] == 1 else False 
                if int(attribute["defindex"]) == 834: TEMPLATE["paintkit"] = attribute["float_value"]
                if int(attribute["defindex"]) == 749: TEMPLATE["wear"] = attribute["float_value"]
                if int(attribute["defindex"]) == 214 and item['quality'] == 5: TEMPLATE["quality2"] = attribute["value"]
                if int(attribute["defindex"]) == 229: TEMPLATE["craftnumber"] = attribute["value"]
                if int(attribute["defindex"]) == 187: TEMPLATE["crateseries"] = attribute["float_value"]
                if 2000 <= int(attribute["defindex"]) <= 2009 and attribute.get("attributes"):
                    for attr in attribute["attributes"]:
                        if int(attr["defindex"]) == 2012: TEMPLATE["target"] = attr["float_value"]
                if attribute.get("is_output") and attribute["is_output"] is True: 
                    TEMPLATE["output"] = attribute["itemdef"]
                    TEMPLATE["outputQuality"] = attribute["quantity"]
                if int(attribute["defindex"]) == 142: TEMPLATE["paint"] = attribute["float_value"]
        
        return SKU.fromObject(TEMPLATE)
