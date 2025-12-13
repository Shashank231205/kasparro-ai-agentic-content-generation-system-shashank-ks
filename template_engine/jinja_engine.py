# template_engine/jinja_engine.py

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class JinjaEngine:
    """
    Simple JSON-safe Jinja template renderer.
    """

    def __init__(self):
        root_dir = Path(__file__).resolve().parents[1]
        templates_dir = root_dir / "templates"

        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=False
        )

    def render_template_file(self, template_path: str, context: dict) -> str:
        """
        Renders a Jinja2 template into a JSON string.
        Ensures the output is valid JSON.
        """

        template_name = Path(template_path).name
        template = self.env.get_template(template_name)

        output = template.render(context)

        # Validate JSON (required for your assignment)
        try:
            json.loads(output)
        except Exception as e:
            raise ValueError(f"Template output is not valid JSON: {e}")

        return output
