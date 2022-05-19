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

x = TF2("apiKey", autoUpdate, updateTime)
# autoUpdate - Automatic update schema (True/False). (Default: False)
# updateTime - Seconds between updates. (Default: 86400 seconds)

# Convert SKU to name
name = x.schema.getNameFromSku(sku)

# Convert name to SKU
sku = x.schema.getSkuFromName(name)
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
```

## Questions/Bugs?
Feel free to contact me if you encounter any issues or have any questions.
Discord (Johnny Black#6363) / [Steam](https://steamcommunity.com/profiles/76561198076771380/)
