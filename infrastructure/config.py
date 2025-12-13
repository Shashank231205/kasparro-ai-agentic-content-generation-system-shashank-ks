# infrastructure/config.py
from pathlib import Path
import os
from dotenv import load_dotenv
import yaml


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
YAML_PATH = ROOT / "config.yaml"

# Load environment variables, if present
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


class Config:
    """Central configuration with layered priority:
       1. .env
       2. config.yaml
       3. safe default values
    """

    # -------- Load YAML (optional) --------
    try:
        if YAML_PATH.exists():
            with YAML_PATH.open("r", encoding="utf-8") as f:
                _cfg = yaml.safe_load(f) or {}
        else:
            _cfg = {}
    except Exception:
        _cfg = {}

    # ============================
    # PATHS
    # ============================

    INPUT_PRODUCT_DATA = (
        os.getenv("INPUT_PRODUCT_DATA")
        or _cfg.get("input", {}).get("product_data")
        or "input/product_data.json"
    )

    TEMPLATE_FAQ = (
        os.getenv("TEMPLATE_FAQ")
        or _cfg.get("templates", {}).get("faq")
        or "templates/faq_template.json"
    )

    TEMPLATE_PRODUCT = (
        os.getenv("TEMPLATE_PRODUCT")
        or _cfg.get("templates", {}).get("product_page")
        or "templates/product_page_template.json"
    )

    TEMPLATE_COMPARISON = (
        os.getenv("TEMPLATE_COMPARISON")
        or _cfg.get("templates", {}).get("comparison")
        or "templates/comparison_page_template.json"
    )

    OUTPUT_FAQ = (
        os.getenv("OUTPUT_FAQ")
        or _cfg.get("outputs", {}).get("faq")
        or "outputs/faq.json"
    )

    OUTPUT_PRODUCT = (
        os.getenv("OUTPUT_PRODUCT")
        or _cfg.get("outputs", {}).get("product_page")
        or "outputs/product_page.json"
    )

    OUTPUT_COMPARISON = (
        os.getenv("OUTPUT_COMPARISON")
        or _cfg.get("outputs", {}).get("comparison")
        or "outputs/comparison_page.json"
    )

    # ============================
    # LLM CONFIG
    # ============================

    # Always prefer .env if present (correct behavior)
    question_model = (
        os.getenv("QUESTION_MODEL")
        or _cfg.get("llm", {}).get("model")
        or "google/flan-t5-large,google/flan-t5-base,google/flan-t5-small"
    )

    max_tokens = int(
        os.getenv("MAX_TOKENS")
        or _cfg.get("llm", {}).get("max_tokens")
        or 256
    )

    temperature = float(
        os.getenv("TEMPERATURE")
        or _cfg.get("llm", {}).get("temperature")
        or 0.3
    )

    min_questions = int(
        os.getenv("MIN_QUESTIONS")
        or _cfg.get("llm", {}).get("min_questions")
        or 15
    )

    # Reviewer expects UPPERCASE names
    QUESTION_MODEL = question_model
    MAX_TOKENS = max_tokens
    TEMPERATURE = temperature
    MIN_QUESTIONS = min_questions
