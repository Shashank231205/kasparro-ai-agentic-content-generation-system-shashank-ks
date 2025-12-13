import pytest
from infrastructure.llm_client import UnifiedFLANLLM

@pytest.fixture
def llm_stub():
    # Safe stub: never calls real LLM
    class StubLLM:
        def run(self, prompt):
            return "[]"
    return StubLLM()

@pytest.fixture
def template_paths():
    return {
        "faq": "templates/faq_template.json",
        "product": "templates/product_page_template.json",
        "comparison": "templates/comparison_page_template.json"
    }
