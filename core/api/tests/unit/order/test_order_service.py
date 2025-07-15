import httpretty

from api.tests.base import BaseAPITestCase
from api.services import OrderService, CartService
from api.models import Order

from api.tests.mocks.payments.razorpay import MockRazorPayRequests


class OrderServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product2 = self.make_model("Product", inventory_count=10)
        self.product3 = self.make_model("Product", inventory_count=10)
        self.buyer_address = self.make_model("BuyerAddress", user=self.user)

    @httpretty.activate
    def test_get_user_orders(self):
        MockRazorPayRequests().mock_razorpay_requests()
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 0)

        # add product1 to the cart
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

        # create order for the user cart
        order = OrderService.create_order_from_cart(user=self.user)
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 1)

    @httpretty.activate
    def test_get_user_order_by_id(self):
        MockRazorPayRequests().mock_razorpay_requests()
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 0)

        # add product1 to the cart
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

        # create order for the user cart
        order = OrderService.create_order_from_cart(user=self.user)
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 1)

        order_by_id = OrderService.get_order_by_id(
            user_id=self.user.id, order_id=order.id
        )
        self.assertEqual(order_by_id, order)

    @httpretty.activate
    def test_create_order_from_cart(self):
        MockRazorPayRequests().mock_razorpay_requests()
        # add product1 to the cart
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

        # create order for the user cart
        order = OrderService.create_order_from_cart(user=self.user)
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 1)

    @httpretty.activate
    def test_update_order_status(self):
        MockRazorPayRequests().mock_razorpay_requests()
        # add product1 to the cart
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=5)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 5)

        # create order for the user cart
        order = OrderService.create_order_from_cart(user=self.user)
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 1)

        new_order_status = Order.StatusChoices.PROCESSING
        order = OrderService.update_order_status(
            user=self.user, order_id=order.id, status=new_order_status
        )
        self.assertEqual(order.status, new_order_status)
