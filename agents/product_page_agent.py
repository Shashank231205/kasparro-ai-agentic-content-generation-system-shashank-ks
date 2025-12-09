import json
from template_engine.engine import TemplateEngine

class ProductPageAgent:
    def __init__(self):
        pass

    def run(self, product, template_path):
        template = TemplateEngine(template_path).template

        product_name = product.get("product_name", "Unknown Product")

        output = {"product_name": product_name}

        for field in template["fields"]:

            if field == "benefits":
                output["benefits"] = {
                    "product_name": product_name,
                    "benefits": product.get("benefits", [])
                }

            elif field == "ingredients":
                output["ingredients"] = {
                    "key_ingredients": product.get("key_ingredients", []),
                    "concentration": product.get("concentration", "")
                }

            elif field == "usage":
                output["usage"] = {
                    "how_to_use": product.get("how_to_use", "")
                }

            elif field == "safety":
                output["safety"] = {
                    "skin_type": product.get("skin_type", []),
                    "side_effects": product.get("side_effects", "")
                }

            elif field == "pricing":
                output["pricing"] = product.get("price", "")

        return output
