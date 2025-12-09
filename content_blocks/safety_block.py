def generate_safety_block(product):
    """
    Safety information: side effects and skin-type notes.
    """
    return {
        "skin_type": product.skin_type,
        "side_effects": product.side_effects
    }
