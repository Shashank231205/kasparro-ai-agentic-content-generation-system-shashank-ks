from agents.question_generation_agent import QuestionGenerationAgent
from agents.parser_agent import ParserAgent

parser = ParserAgent()
product = parser.run("input/product_data.json")

q_agent = QuestionGenerationAgent()
questions = q_agent.run(product)

print("\n=== GENERATED QUESTIONS ===")
for q in questions:
    print(q)
