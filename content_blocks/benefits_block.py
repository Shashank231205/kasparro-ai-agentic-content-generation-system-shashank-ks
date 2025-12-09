def generate_benefits_block(product):
    """
    Returns structured benefits derived directly from product data.
    No external assumptions allowed.
    """
    return {
        "product_name": product.product_name,
        "benefits": product.benefits
    }
