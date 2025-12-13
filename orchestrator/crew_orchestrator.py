# orchestrator/crew_orchestrator.py

import json
from infrastructure.llm_client import LLMClient
from infrastructure.config import Config

from agents.faq_page_agent import FAQAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_page_agent import ComparisonPageAgent


class HybridOrchestrator:
    """
    Final orchestrator.
    CrewAI is part of architecture, NOT runtime execution.
    """

    def __init__(self, debug=False):
        self.debug = debug
        self.llm = LLMClient().as_crew_llm()

        self.faq_agent = FAQAgent(self.llm)
        self.product_agent = ProductPageAgent(self.llm)
        self.compare_agent = ComparisonPageAgent(self.llm)

    def run(self):
        # -----------------------------
        # Load product input
        # -----------------------------
        with open(Config.INPUT_PRODUCT_DATA, "r", encoding="utf-8") as f:
            product = json.load(f)

        if self.debug:
            print("🔵 Loaded product:", product.get("product_name"))

        # -----------------------------
        # Generate outputs (NO Crew loop)
        # -----------------------------
        faq_list = self.faq_agent.generate_faq(product)
        faq_json = self.faq_agent.render_faq_page(
            product, faq_list, Config.TEMPLATE_FAQ
        )

        product_json = self.product_agent.run(
            product, Config.TEMPLATE_PRODUCT
        )

        comparison_json = self.compare_agent.run(
            product, product, Config.TEMPLATE_COMPARISON
        )

        # -----------------------------
        # Save outputs
        # -----------------------------
        with open(Config.OUTPUT_FAQ, "w", encoding="utf-8") as f:
            f.write(faq_json)

        with open(Config.OUTPUT_PRODUCT, "w", encoding="utf-8") as f:
            f.write(product_json)

        with open(Config.OUTPUT_COMPARISON, "w", encoding="utf-8") as f:
            f.write(comparison_json)

        print("✅ All outputs generated successfully")

        return {
            "faq_page": faq_json,
            "product_page": product_json,
            "comparison_page": comparison_json,
            "questions": faq_list,
        }
