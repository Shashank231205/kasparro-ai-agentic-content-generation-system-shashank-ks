from agents.faq_page_agent import FAQAgent

def test_faq_minimum_15(llm_stub):
    product = {
        "product_name": "Test Serum",
        "key_ingredients": ["Vitamin C"],
        "benefits": ["Brightening"]
    }

    agent = FAQAgent(llm_stub)
    faqs = agent.generate_faq(product)

    assert isinstance(faqs, list)
    assert len(faqs) >= 15
