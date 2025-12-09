import json
from template_engine.engine import TemplateEngine

class ComparisonPageAgent:
    def run(self, product_a, product_b, template_path):
        engine = TemplateEngine(template_path)

        comparison = {
            "product_a": {
                "name": product_a.get("product_name"),
                "price": product_a.get("price"),
                "ingredients": product_a.get("key_ingredients"),
                "benefits": product_a.get("benefits")
            },
            "product_b": {
                "name": product_b.get("product_name"),
                "price": product_b.get("price"),
                "ingredients": product_b.get("key_ingredients"),
                "benefits": product_b.get("benefits")
            },
            "comparison_summary": {
                "price_difference": f"{product_a.get('price')} vs {product_b.get('price')}",
                "shared_ingredients": list(
                    set(product_a.get("key_ingredients", []))
                    & set(product_b.get("key_ingredients", []))
                )
            }
        }

        return engine.fill_template(
            product_a=comparison["product_a"],
            product_b=comparison["product_b"],
            comparison=comparison["comparison_summary"]
        )
