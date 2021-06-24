def _cart_id(request):
    """Cart_id for not authorized users."""
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart
