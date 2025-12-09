import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class QuestionGenerationAgent:
    """
    Hybrid LLM question generator:
    - Try BART first (offline LLM)
    - Extract usable questions
    - If BART output is poor, fallback to handcrafted product-aware questions
    - ALWAYS merge BART + fallback to ensure coverage of all categories
    """

    def __init__(self):
        print("Loading BART for Question Generation...")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")
        self.model.eval()

        self.categories = [
            "Usage",
            "Safety",
            "Ingredients",
            "Pricing",
            "Benefits",
            "Comparison",
        ]

    def _generate_with_bart(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            top_p=0.95,
            top_k=50,
            temperature=0.8,
            no_repeat_ngram_size=2,
        )

        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def _fallback_questions(self, product: dict):
        """High-quality deterministic questions when BART fails."""
        name = product.get("product_name", "this product")
        ingredients = ", ".join(product.get("key_ingredients", []))
        benefits = ", ".join(product.get("benefits", []))

        base = [
            # USAGE
            ("Usage", f"How should I apply {name} for best results?"),
            ("Usage", f"How often should {name} be used in my routine?"),

            # SAFETY
            ("Safety", f"Is {name} suitable for sensitive or acne-prone skin?"),
            ("Safety", f"Can {name} cause any irritation or purging?"),

            # INGREDIENTS
            ("Ingredients", f"What are the key ingredients in {name} ({ingredients})?"),
            ("Ingredients", f"Are there any irritating ingredients in {name}?"),

            # PRICING
            ("Pricing", f"Is {name} worth its price compared to other serums?"),
            ("Pricing", f"Does {name} offer good value for money?"),

            # BENEFITS
            ("Benefits", f"What visible results can I expect from using {name} ({benefits})?"),
            ("Benefits", f"How long does it take to see results with {name}?"),

            # COMPARISON
            ("Comparison", f"How does {name} compare to other Vitamin C serums?"),
            ("Comparison", f"Why should I choose {name} over cheaper alternatives?"),
        ]

        return [{"category": c, "question": q} for c, q in base]

    def _extract_questions_from_bart(self, text: str):
        """Extract lines ending with '?' and reject junk."""
        questions = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Remove numbering ("1. What…")
            if "." in line[:4]:
                try:
                    idx = int(line.split(".")[0])
                    line = line[line.find(".")+1:].strip()
                except:
                    pass

            # Only accept actual questions
            if line.endswith("?"):
                questions.append(line)

        return questions

    def _categorize(self, q: str):
        """Simple keyword-based categorization."""
        lq = q.lower()
        if any(w in lq for w in ["use", "apply", "routine", "how often"]):
            return "Usage"
        if any(w in lq for w in ["safe", "sensitive", "side effect", "irritation"]):
            return "Safety"
        if any(w in lq for w in ["ingredient", "contain", "formula", "vitamin"]):
            return "Ingredients"
        if any(w in lq for w in ["price", "cost", "expensive", "cheap", "value"]):
            return "Pricing"
        if any(w in lq for w in ["benefit", "result", "effect", "improvement"]):
            return "Benefits"
        if any(w in lq for w in ["compare", "better than", "alternative"]):
            return "Comparison"

        # fallback: assign by index bucket
        return "General"

    def run(self, product: dict):
        """Final orchestration: BART → extract → fallback merge → category structuring."""

        product_name = product.get("product_name")
        ingredients = ", ".join(product.get("key_ingredients", []))
        benefits = ", ".join(product.get("benefits", []))

        prompt = (
            f"Generate 12 different customer questions about this skincare product.\n"
            f"Each question MUST end with a '?'. One per line.\n\n"
            f"Product: {product_name}\n"
            f"Ingredients: {ingredients}\n"
            f"Benefits: {benefits}\n\n"
            "Questions:\n"
        )

        # Step 1: try BART
        try:
            bart_output = self._generate_with_bart(prompt)
            bart_questions = self._extract_questions_from_bart(bart_output)
        except Exception:
            bart_questions = []

        # Step 2: fallback + merge
        fallback = self._fallback_questions(product)

        final_questions = []

        # use BART questions first (few but still valid)
        for q in bart_questions:
            final_questions.append({
                "category": self._categorize(q),
                "question": q
            })

        # ensure minimum 12 by adding fallback
        for item in fallback:
            if len(final_questions) >= 12:
                break
            final_questions.append(item)

        return final_questions
