from orchestrator.dag_orchestrator import DAGOrchestrator


def main():
    print("\n🚀 Starting Multi-Agent Content Generation Pipeline...\n")

    orchestrator = DAGOrchestrator()
    outputs = orchestrator.run()

    print("\n✅ Pipeline completed successfully!")
    print("📄 Generated files:")
    print(" - outputs/faq.json")
    print(" - outputs/product_page.json")
    print(" - outputs/comparison_page.json")
    print("\nDone.\n")


if __name__ == "__main__":
    main()
