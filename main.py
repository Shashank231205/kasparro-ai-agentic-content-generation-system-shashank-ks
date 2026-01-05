import os
os.environ["LANGCHAIN_VERBOSE"] = "true"
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = ""
from orchestrator.langchain_orchestrator import LangChainOrchestrator


def main():
    print("🚀 Starting LangChain Agentic Pipeline")

    orch = LangChainOrchestrator()
    result = orch.run()

    print("\n==============================")
    print("✅ Pipeline completed")
    print("==============================\n")

    print("FINAL AGENT RESPONSE:\n")
    print(result)


if __name__ == "__main__":
    main()
