from orchestrator.crew_orchestrator import HybridOrchestrator

def test_orchestrator_outputs_exist():
    orch = HybridOrchestrator()
    result = orch.run()

    assert "faq_page" in result
    assert "product_page" in result
    assert "comparison_page" in result
