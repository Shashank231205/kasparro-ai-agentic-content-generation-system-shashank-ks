from agents.parser_agent import ParserAgent

parser = ParserAgent()
product = parser.run("input/product_data.json")

print("\n=== PARSED PRODUCT ===")
for k, v in product.items():
    print(f"{k}: {v}")
