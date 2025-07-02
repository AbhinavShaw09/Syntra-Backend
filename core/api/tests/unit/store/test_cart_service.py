from ...base import BaseAPITestCase
from api.services import CartService


class ProductServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product1 = self.make_model("Product", inventory_count=10)
        self.product2 = self.make_model("Product", inventory_count=10)

    def test_get_user_cart(self):
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 0)
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=1)
        self.assertEqual(user_cart.count(), 1)

    def test_add_to_cart(self):
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

    def test_update_cart_item(self):
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

        CartService.update_cart_item(
            user=self.user, item_id=user_cart[0].id, quantity=10
        )
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 10)

    def test_remove_from_cart(self):
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

        CartService.remove_from_cart(user=self.user, item_id=user_cart[0].id)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 0)

    def test_get_cart_total(self):
        item_quantity = 5
        CartService.add_to_cart(
            user=self.user, product_id=self.product1.id, quantity=item_quantity
        )
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, item_quantity)

        cart_total = CartService.get_cart_total(user=self.user)
        self.assertEqual(cart_total, self.product1.price * item_quantity)
