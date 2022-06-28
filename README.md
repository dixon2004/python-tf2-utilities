# python-tf2-utilities
Get information about TF2 items, effects, skins and more. 
Inspired by [TF2autobot's node-tf2-schema](https://github.com/TF2Autobot/node-tf2-schema) and [TF2autobot's node-tf2-sku](https://github.com/TF2Autobot/node-tf2-sku).

## Installation
```py
pip install tf2-utilities
```

## Examples
```py
from tf2utilities.main import TF2

tf2 = TF2("apiKey", autoUpdate, updateTime).schema
# autoUpdate - Automatic update schema (True/False). (Default: False)
# updateTime - Seconds between updates. (Default: 86400 seconds)

# Convert SKU to name
name = tf2.getNameFromSku(sku)

# Convert name to SKU
sku = tf2.getSkuFromName(name)

# Get TF2 schema as json
schema = tf2.toJSON()
```

```py
from tf2utilities.sku import SKU

# Item object example
itemObject = {
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

# Convert SKU to item object
itemObject = SKU.fromString(sku)

# Convert item object to SKU
sku = SKU.fromObject(itemObject)

# Convert item data from Steam Web API to SKU
sku = SKU.fromAPI(itemData)
```

## Questions/Bugs?
Feel free to contact me if you encounter any issues or have any questions.
Discord (Johnny Black#6363) / [Steam](https://steamcommunity.com/profiles/76561198076771380/)
