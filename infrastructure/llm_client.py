import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LLMClient:
    def __init__(self, model_name="google/flan-t5-base"):
        self.model_name = model_name
        print(f"LLM MODE: LOCAL OFFLINE ({self.model_name})")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.device = torch.device("cpu")
            self.model.to(self.device)
            self.mode = "local"
        except:
            print("⚠️ FLAN-T5 load failed → MOCK MODE")
            self.mode = "mock"

    def generate(self, prompt: str):
        if self.mode == "mock":
            return self._mock(prompt)

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=250,
                temperature=0.7,
                early_stopping=True
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except:
            return self._mock(prompt)

    @staticmethod
    def _mock(prompt: str):
        return f"[MOCK RESPONSE] {prompt[:80]}..."
