# agents/template_selection_agent.py
from agents.base_agent import BaseAgent
from infrastructure.config import Config


class TemplateSelectionAgent(BaseAgent):
    """Returns template paths from config."""

    def run(self):
        return {
            "faq": Config.TEMPLATE_FAQ,
            "product_page": Config.TEMPLATE_PRODUCT,
            "comparison_page": Config.TEMPLATE_COMPARISON,
        }
