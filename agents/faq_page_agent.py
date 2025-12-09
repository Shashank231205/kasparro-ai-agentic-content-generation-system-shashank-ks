# agents/faq_page_agent.py

import json
from template_engine.engine import TemplateEngine
from infrastructure.llm_client import LLMClient


class FAQPageAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, product, template_path, questions=None):
        engine = TemplateEngine(template_path)

        # If questions not provided, generate them here (fallback mode)
        if questions is None:
            prompt = f"""
            Generate 10 FAQs for the following skincare product.
            Categories:
            - Usage
            - Safety
            - Ingredients
            - Pricing
            - Comparison

            Product info:
            {json.dumps(product, indent=2)}
            """

            faq_text = self.llm.generate(prompt)
            faq_items = []
            for line in faq_text.split("\n"):
                line = line.strip()
                if not line or "." not in line:
                    continue
                q = line[line.find(".") + 1 :].strip()
                faq_items.append({"category": "general", "question": q})
        else:
            # Use questions from QuestionGenerationAgent
            faq_items = questions

        return engine.fill_template(
            product_name=product.get("product_name"),
            faq_items=faq_items,
            benefits={
                "product_name": product.get("product_name"),
                "benefits": product.get("benefits", [])
            },
            ingredients={
                "key_ingredients": product.get("key_ingredients", []),
                "concentration": product.get("concentration")
            },
            usage={
                "how_to_use": product.get("how_to_use")
            },
            safety={
                "skin_type": product.get("skin_type", []),
                "side_effects": product.get("side_effects")
            },
            pricing=product.get("price")
        )
