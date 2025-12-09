import os

class TemplateSelectionAgent:
    """
    Selects which JSON template files the content generator should use.
    """

    def __init__(self):
        self.template_dir = "templates"

    def run(self):
        return {
            "faq": os.path.join(self.template_dir, "faq_template.json"),
            "product_page": os.path.join(self.template_dir, "product_page_template.json"),
            "comparison_page": os.path.join(self.template_dir, "comparison_template.json")
        }
