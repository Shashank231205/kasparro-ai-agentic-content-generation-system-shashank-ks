def compare_products_block(productA, productB):
    """
    Compares two products in a structured, rule-based manner.
    
    NOTE:
    - No external assumptions allowed.
    - Only compare fields present in both models.
    """
    return {
        "product_a": {
            "name": productA.product_name,
            "price": productA.price,
            "ingredients": productA.key_ingredients,
            "benefits": productA.benefits
        },
        "product_b": {
            "name": productB.product_name,
            "price": productB.price,
            "ingredients": productB.key_ingredients,
            "benefits": productB.benefits
        },
        "comparison_summary": {
            "price_difference": f"{productA.price} vs {productB.price}",
            "shared_ingredients": list(set(productA.key_ingredients) & set(productB.key_ingredients))
        }
    }
