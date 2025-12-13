# main.py
from orchestrator.crew_orchestrator import HybridOrchestrator

def main():
    orch = HybridOrchestrator(debug=True)
    final = orch.run()

    print("\nFINAL OUTPUT KEYS:", final.keys())

if __name__ == "__main__":
    main()
