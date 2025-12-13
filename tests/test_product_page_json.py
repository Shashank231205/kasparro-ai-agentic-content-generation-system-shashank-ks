import json
from agents.product_page_agent import ProductPageAgent

def test_product_page_valid_json(llm_stub, template_paths):
    agent = ProductPageAgent(llm_stub)

    product = {
        "product_name": "GlowBoost",
        "benefits": ["Brightening"],
        "key_ingredients": ["Vitamin C"],
        "how_to_use": "Apply daily",
        "side_effects": "None",
        "skin_type": ["All"],
        "price": "₹699"
    }

    out = agent.run(product, template_paths["product"])
    parsed = json.loads(out)

    assert parsed["product_name"] == "GlowBoost"
