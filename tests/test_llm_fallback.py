import json
from infrastructure.llm_client import LLMClient

def test_llm_fallback_returns_json(monkeypatch):
    client = LLMClient()

    monkeypatch.setattr(
        "infrastructure.llm_client.FlanSingleton.load",
        lambda: None
    )

    out = client.generate("test")
    data = json.loads(out)

    assert isinstance(data, list)
    assert len(data) >= 15
