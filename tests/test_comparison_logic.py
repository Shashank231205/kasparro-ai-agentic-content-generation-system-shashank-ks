import json
from agents.comparison_page_agent import ComparisonPageAgent

def test_shared_ingredients_computed(llm_stub, template_paths):
    agent = ComparisonPageAgent(llm_stub)

    p1 = {"product_name": "A", "price": "₹100", "key_ingredients": ["X", "Y"]}
    p2 = {"product_name": "B", "price": "₹200", "key_ingredients": ["Y", "Z"]}

    out = agent.run(p1, p2, template_paths["comparison"])
    data = json.loads(out)

    assert data["comparison"]["shared_ingredients"] == ["Y"]
