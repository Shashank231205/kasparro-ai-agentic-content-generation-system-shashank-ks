# agents/base_agent.py
from typing import Any, Optional
from template_engine.jinja_engine import JinjaEngine


class AgentError(Exception):
    pass

class BaseAgent:
    def __init__(self, llm=None):
        """
        Every agent gets a shared LLM (optional) and a template engine.
        """
        self.llm = llm
        self.engine = JinjaEngine()
