# orchestrator/dag_orchestrator.py

import json
from agents.parser_agent import ParserAgent
from agents.question_generation_agent import QuestionGenerationAgent
from agents.faq_page_agent import FAQPageAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_page_agent import ComparisonPageAgent


class DAGOrchestrator:
    """
    Controls the full multi-agent pipeline:

    1. Parse product data
    2. Generate categorized FAQ questions
    3. Build FAQ page JSON
    4. Build Product Description JSON
    5. Build Comparison JSON (A vs A)
    6. Save outputs
    """

    def __init__(self):
        self.parser_agent = ParserAgent()
        self.q_agent = QuestionGenerationAgent()
        self.faq_agent = FAQPageAgent()
        self.product_agent = ProductPageAgent()
        self.comparison_agent = ComparisonPageAgent()

    def run(self):

        # STEP 1: Load & parse raw product data
        product = self.parser_agent.run("input/product_data.json")

        # STEP 2: Generate categorized questions
        questions = self.q_agent.run(product)

        # STEP 3: Build FAQ Page
        faq_page = self.faq_agent.run(
            product=product,
            template_path="templates/faq_template.json",
            questions=questions
        )

        # STEP 4: Build Product Page
        product_page = self.product_agent.run(
            product=product,
            template_path="templates/product_page_template.json"
        )

        # STEP 5: Build Comparison Page (self vs self)
        comparison_page = self.comparison_agent.run(
            product_a=product,
            product_b=product,
            template_path="templates/comparison_page_template.json"
        )

        # STEP 6: Save outputs
        self._write_json("outputs/faq.json", faq_page)
        self._write_json("outputs/product_page.json", product_page)
        self._write_json("outputs/comparison_page.json", comparison_page)

        return {
            "faq_page": faq_page,
            "product_page": product_page,
            "comparison_page": comparison_page
        }

    @staticmethod
    def _write_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
