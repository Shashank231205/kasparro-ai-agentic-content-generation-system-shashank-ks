# agents/question_generation_agent.py

import json
import re
from typing import Dict, List, Any
from agents.base_agent import BaseAgent, AgentError
from infrastructure.json_llm_wrapper import JSONForcingLLM
from infrastructure.config import Config


class QuestionGenerationAgent(BaseAgent):
    """
    Professional FAQ generator.
    Produces strictly valid JSON and ensures a minimum number of FAQs.
    """

    CATEGORIES = [
        "Usage", "Safety", "Ingredients",
        "Benefits", "Pricing", "Comparison", "General"
    ]

    def __init__(self, llm=None):
        super().__init__(llm)
        self.json_llm = JSONForcingLLM()
        self.min_faqs = Config.MIN_QUESTIONS

    # ----------------------------------------------------
    # BUILD PROMPT
    # ----------------------------------------------------
    def _prompt(self, product: Dict[str, Any]) -> str:
        return f"""
You are an expert FAQ generator.

Return ONLY a **pure JSON array**, no extra text.

Each object must have this exact shape:
{{
  "category": "One of {self.CATEGORIES}",
  "question": "A short, clear FAQ question"
}}

Write **20 FAQs** about this product.

PRODUCT DETAILS:
{json.dumps(product, indent=2, ensure_ascii=False)}

Return ONLY a JSON array.
"""

    # ----------------------------------------------------
    # FALLBACK GENERATOR
    # ----------------------------------------------------
    def _fallback_questions(self, product: Dict[str, Any], count: int) -> List[Dict[str, str]]:
        name = product.get("product_name", "the product")
        ingredients = product.get("key_ingredients", [])
        ing_text = ", ".join(ingredients) if ingredients else "its active ingredients"

        templates = [
            ("Usage", f"How should I apply {name}?"),
            ("Usage", f"Can I use {name} daily?"),
            ("Safety", f"Is {name} safe for sensitive skin?"),
            ("Safety", f"Does {name} have any side effects?"),
            ("Ingredients", f"What are the key ingredients in {name}?"),
            ("Ingredients", f"How does {ing_text} benefit the skin?"),
            ("Benefits", f"What results can I expect from {name}?"),
            ("Benefits", f"How long until I see visible improvements from using {name}?"),
            ("Pricing", f"What is the price of {name}?"),
            ("Pricing", f"Is {name} available in different sizes?"),
            ("Comparison", f"How does {name} compare with similar skincare products?"),
            ("General", f"Who can benefit most from using {name}?"),
        ]

        out = []
        idx = 0
        while len(out) < count:
            cat, q = templates[idx % len(templates)]
            out.append({"category": cat, "question": q})
            idx += 1

        return out

    # ----------------------------------------------------
    # MAIN RUN LOGIC
    # ----------------------------------------------------
    def run(self, product: Dict[str, Any]) -> List[Dict[str, str]]:
        try:
            prompt = self._prompt(product)

            # Request LLM output using strict JSON forcing
            fallback = self._fallback_questions(product, self.min_faqs)
            llm_data = self.json_llm.generate_json(prompt, fallback)

            cleaned = []
            seen = set()

            for item in llm_data:
                if not isinstance(item, dict):
                    continue

                cat = str(item.get("category", "General")).strip().title()
                if cat not in self.CATEGORIES:
                    cat = "General"

                q = str(item.get("question", "")).strip()
                if not q:
                    continue

                key = (cat, q.lower())
                if key in seen:
                    continue

                seen.add(key)
                cleaned.append({"category": cat, "question": q})

                if len(cleaned) >= self.min_faqs:
                    break

            # If still fewer than required → pad using fallback
            if len(cleaned) < self.min_faqs:
                needed = self.min_faqs - len(cleaned)
                extra = self._fallback_questions(product, needed)
                for f in extra:
                    key = (f["category"], f["question"].lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    cleaned.append(f)
                    if len(cleaned) >= self.min_faqs:
                        break

            return cleaned[:self.min_faqs]

        except Exception as e:
            raise AgentError(f"QuestionGenerationAgent error: {e}")
