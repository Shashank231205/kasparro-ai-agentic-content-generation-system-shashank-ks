from agents.faq_page_agent import FAQAgent

def test_faq_schema_valid(llm_stub):
    product = {"product_name": "X"}
    agent = FAQAgent(llm_stub)
    faqs = agent.generate_faq(product)

    for item in faqs:
        assert "category" in item
        assert "question" in item
        assert isinstance(item["question"], str)
