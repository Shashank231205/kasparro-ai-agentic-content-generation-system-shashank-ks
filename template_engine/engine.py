import json

class TemplateEngine:
    def __init__(self, template_path):
        text = open(template_path, "r", encoding="utf-8").read()

        # If template contains placeholders → treat as raw text
        if "{{" in text:
            self.template_str = text
            self.template = None
        else:
            # Otherwise load as JSON (for product_page template)
            self.template = json.loads(text)
            self.template_str = None

    def fill_template(self, **kwargs):
        if self.template_str is None:
            raise ValueError("Cannot call fill_template() on a JSON template.")

        result = self.template_str

        for key, value in kwargs.items():
            placeholder = "{{ " + key + " }}"
            result = result.replace(placeholder, json.dumps(value))

        return json.loads(result)
