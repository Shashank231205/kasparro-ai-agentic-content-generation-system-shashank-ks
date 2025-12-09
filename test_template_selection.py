from agents.template_selection_agent import TemplateSelectionAgent
import json

selector = TemplateSelectionAgent()
templates = selector.run()

print("\n=== TEMPLATE SELECTION OUTPUT ===")
print(json.dumps(templates, indent=4))
