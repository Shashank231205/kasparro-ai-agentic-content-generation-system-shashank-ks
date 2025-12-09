from infrastructure.llm_client import LLMClient

llm = LLMClient()
print(llm.generate("Write 2 FAQ questions about Vitamin C serum."))
