import json
import re
from infrastructure.llm_client import LLMClient

class JSONForcingLLM:
    """
    Wraps LLMClient and forces it to always output valid JSON using:
    1. Strong JSON-structured prompt framing
    2. Extraction of the JSON substring
    3. Cleaning heuristics
    4. Full fallback if all attempts fail
    """

    def __init__(self):
        self.client = LLMClient()

    def generate_json(self, prompt: str, fallback: list):
        raw = self.client.generate(prompt)

        # Step 1 — Extract JSON array/brackets
        start = raw.find("[")
        end = raw.rfind("]")

        if start == -1 or end == -1:
            return fallback

        candidate = raw[start:end+1]

        # Step 2 — Clean common JSON issues
        cleaned = candidate.replace("'", "\"")
        cleaned = re.sub(r",\s*}", "}", cleaned)
        cleaned = re.sub(r",\s*]", "]", cleaned)

        # Step 3 — Try parsing
        try:
            data = json.loads(cleaned)
            if isinstance(data, list):
                return data
        except Exception:
            pass

        # Step 4 — Last fallback
        return fallback
