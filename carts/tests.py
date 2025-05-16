from django.test import TestCase

# Create your tests here.

from carts.models import Cart
def test_cart_remove(client, cart):
    """
    Test removing item from cart.
    """
    client.force_login(cart.user) if cart.user else None
    response = client.post(
        '/carts/remove/',
        {'cart_id': cart.id},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert response.status_code == 200
    assert not Cart.objects.filter(id=cart.id).exists()
    assert response.json()['message'] == "Машину видалено"