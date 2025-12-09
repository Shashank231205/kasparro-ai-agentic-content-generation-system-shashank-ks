def generate_ingredients_block(product):
    """
    Structures the ingredient list for template consumption.
    """
    return {
        "key_ingredients": product.key_ingredients,
        "concentration": product.concentration
    }
