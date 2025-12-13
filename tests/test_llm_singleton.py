from infrastructure.llm_client import LLMClient

def test_llm_singleton_instance():
    a = LLMClient()
    b = LLMClient()
    assert a is b
