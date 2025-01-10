# python-tf2-utilities
A fast, reliable, and easy-to-use Python library for accessing detailed Team Fortress 2 (TF2) data, including items, skins, effects, and more. Built for developers, this library simplifies retrieving and managing TF2 assets, with minimal setup and optimized performance.

Inspired by [TF2autobot's node-tf2-schema](https://github.com/TF2Autobot/node-tf2-schema) and [TF2autobot's node-tf2-sku](https://github.com/TF2Autobot/node-tf2-sku), this library supports a wide range of TF2-related applications.

## Key Features
- **Item Management:** Easily convert between item SKUs, names, and object formats.
- **Schema Integration:** Access and manipulate detailed TF2 schema data, such as item attributes, qualities, and effects.
- **Comprehensive Tools:** Work with unusual effects, paint kits, skins, crate series, crafting recipes, and trade configurations.
- **Lightweight Mode:** Optimize performance by only loading essential schema data for resource-constrained applications.
- **Automatic Updates:** Automatically stay up to date with schema changes through configurable update intervals.
- **User-Friendly API:** Simplify development with clean, consistent, and intuitive methods.

## Installation
Install the library using pip:
```py
pip install tf2-utilities
```

### Prerequisites:
- Python 3.9 or later
- A Steam Web API key (obtain it from [here](https://steamcommunity.com/dev/apikey))

## Getting Started

### Initialize the Library
To initialize the schema, you’ll need your Steam Web API key:
```py
from tf2utilities.main import TF2

# Initialize the TF2 utilities with your Steam API key and settings
schema = TF2(
    api_key="your_steam_api_key",  # Your Steam Web API key
    auto_update=True,           # Enable automatic schema updates
    update_time=86400,          # Update interval in seconds (default: 1 day)
    lite=False                  # Enable lightweight mode (default: False)
).schema
```

### Common Use Cases

- Convert Item SKU to Item Name
```py
item_name = schema.get_name_from_sku("5021;6")
print(item_name)  # Output: "Mann Co. Supply Crate Key"
```

- Convert Item Name to Item SKU
```py
item_sku = schema.get_sku_from_name("Mann Co. Supply Crate Key")
print(item_sku)  # Output: "5021;6"
```

- Retrieve TF2 Schema as JSON
```py
schema_data = schema.to_json()
print(schema_data) # Output: JSON representation of the schema data
```

### SKU Utilities

- Convert Item SKU to Item Object
```py
from tf2utilities.sku import SKU

item_object = SKU.from_string("5021;6")
print(item_object) # Output: Item object representing the SKU
```

- Convert Item Object to Item SKU
```py
item_object = {
    "defindex": 5021,
    "quality": 6,
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
item_sku = SKU.from_object(item_object)
print(item_sku) # Output: "5021;6"
```

- Convert Steam API Data to Item SKU
```py
item_sku = SKU.from_API(item_data)
print(item_sku) # Output: SKU based on API data
```

## Configuration
| Parameter      | Description                                          | Default        |
|----------------|------------------------------------------------------|----------------|
| `api_key`      | Your Steam Web API key.                              | None           |
| `auto_update`  | Enable or disable automatic schema updates.          | False          |
| `update_time`  | Time interval (in seconds) between schema updates.   | 86400 (1 day)  |
| `lite`         | Enable lightweight mode for reduced memory usage.    | False          |

## Contributing
We welcome contributions! If you’d like to improve the library, fix bugs, or add features, please fork the repository, create a branch, and submit a pull request. For ideas or issues, feel free to open an issue on GitHub.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
