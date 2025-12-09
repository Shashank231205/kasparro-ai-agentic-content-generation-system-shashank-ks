import json
from infrastructure.llm_client import LLMClient

class QuestionGenerationAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, product):

        prompt = f"""
Generate 8 customer questions about the product below.
WRITE THEM AS BULLET POINTS.

Product name: {product['product_name']}
Benefits: {', '.join(product['benefits'])}
Ingredients: {', '.join(product['key_ingredients'])}

Example format:
- What does this serum do?
- Is it safe for oily skin?
- How long before I see results?

Now generate 8 questions:
"""

        raw = self.llm.generate(prompt)

        # Extract bullets
        questions_raw = []
        for line in raw.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                q = line[1:].strip()
                if q.endswith("?"):
                    questions_raw.append(q)

        # If FLAN gives fewer than 8, fill remaining
        while len(questions_raw) < 8:
            questions_raw.append("Auto-generated question?")

        categories = [
            "Usage", "Safety", "Ingredients",
            "Pricing", "Benefits", "Comparison"
        ]

        final = []
        for i, q in enumerate(questions_raw[:8]):
            final.append({
                "category": categories[i % len(categories)],
                "question": q
            })

        return final
