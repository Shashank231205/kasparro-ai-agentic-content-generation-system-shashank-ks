import json
from langchain_core.tools import Tool
from langchain.agents import create_structured_chat_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from infrastructure.llm_client import LLMClient
from infrastructure.config import Config
from agents.faq_page_agent import FAQAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_page_agent import ComparisonPageAgent


class LangChainOrchestrator:
    def __init__(self):
        print("🚀 Using Groq LLM")
        self.llm = LLMClient().as_langchain_llm()

        self.faq_agent = FAQAgent(self.llm)
        self.product_agent = ProductPageAgent(self.llm)
        self.compare_agent = ComparisonPageAgent(self.llm)

        # 🧠 TOOL MEMORY — prevents infinite loops
        self.tool_state = {
            "faq": False,
            "product": False,
            "comparison": False
        }

        # ===================== TOOLS =====================
        self.tools = [
            Tool(
                name="generate_faq",
                func=self._faq_tool,
                description="Generate FAQ page. Input must be product JSON string"
            ),
            Tool(
                name="generate_product_page",
                func=self._product_tool,
                description="Generate product page. Input must be product JSON string"
            ),
            Tool(
                name="generate_comparison",
                func=self._comparison_tool,
                description="Generate comparison page. Input must be product JSON string"
            )
        ]

        # ===================== PROMPT =====================
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a tool calling AI.\n\n"
             "You must call ALL tools exactly once.\n"
             "When all tools return DONE, output Final.\n\n"
             "Available tools:\n{tools}\n\n"
             "Tool names:\n{tool_names}\n\n"
             "Reply ONLY in JSON.\n\n"
             "Tool call format:\n"
             "{{\"action\":\"tool_name\",\"action_input\":\"json\"}}\n\n"
             "Final format:\n"
             "{{\"action\":\"Final\",\"action_input\":\"done\"}}\n\n"
             "Never repeat a tool that already returned DONE.\n"
             "Never explain.\n"
             "Never output python.\n"
             "Never output English."
            ),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

        self.agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=False,
            max_iterations=10
        )

    # ===================== TOOLS =====================

    def _faq_tool(self, product_json: str):
        if self.tool_state["faq"]:
            return "FAQ_ALREADY_DONE"

        print("🟢 TOOL: FAQ")
        product = json.loads(product_json)
        faqs = self.faq_agent.generate_faq(product)
        rendered = self.faq_agent.render_faq_page(product, faqs, Config.TEMPLATE_FAQ)
        with open(Config.OUTPUT_FAQ, "w", encoding="utf-8") as f:
           f.write(rendered)


        self.tool_state["faq"] = True
        return "FAQ_DONE"

    def _product_tool(self, product_json: str):
        if self.tool_state["product"]:
            return "PRODUCT_ALREADY_DONE"

        print("🟢 TOOL: PRODUCT")
        product = json.loads(product_json)
        rendered = self.product_agent.run(product, Config.TEMPLATE_PRODUCT)
        with open(Config.OUTPUT_PRODUCT, "w", encoding="utf-8") as f:
           f.write(rendered)


        self.tool_state["product"] = True
        return "PRODUCT_DONE"

    def _comparison_tool(self, product_json: str):
        if self.tool_state["comparison"]:
            return "COMPARE_ALREADY_DONE"

        print("🟢 TOOL: COMPARISON")
        product = json.loads(product_json)
        rendered = self.compare_agent.run(product, product, Config.TEMPLATE_COMPARISON)
        with open(Config.OUTPUT_COMPARISON, "w", encoding="utf-8") as f:
           f.write(rendered)


        self.tool_state["comparison"] = True
        return "COMPARE_DONE"

    # ===================== RUN =====================

    def run(self):
        product = json.load(open(Config.INPUT_PRODUCT_DATA, "r", encoding="utf-8"))

        prompt = (
            "Call all tools to generate all pages.\n\n"
            "Product JSON:\n"
            + json.dumps(product)
        )

        result = self.executor.invoke({
            "input": prompt,
            "agent_scratchpad": ""
        })
        
        if all(self.tool_state.values()):
           print("\n🛑 All tools executed — stopping agent.\n")

        return {
            "faq": Config.OUTPUT_FAQ,
            "product": Config.OUTPUT_PRODUCT,
            "comparison": Config.OUTPUT_COMPARISON,
            "agent_result": result
        }
