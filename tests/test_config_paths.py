from infrastructure.config import Config

def test_config_paths_defined():
    assert Config.INPUT_PRODUCT_DATA
    assert Config.TEMPLATE_FAQ
    assert Config.OUTPUT_FAQ
