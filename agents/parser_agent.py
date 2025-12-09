# agents/parser_agent.py

import json
from typing import Dict, Any


class ParserAgent:
    """
    Reads and normalizes raw product data from JSON into
    a clean internal product representation.
    """

    def run(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Basic validation + defaults (can be extended)
        product = {
            "product_name": data.get("product_name", ""),
            "concentration": data.get("concentration", ""),
            "skin_type": data.get("skin_type", []),
            "key_ingredients": data.get("key_ingredients", []),
            "benefits": data.get("benefits", []),
            "how_to_use": data.get("how_to_use", ""),
            "side_effects": data.get("side_effects", ""),
            "price": data.get("price", "")
        }

        return product
