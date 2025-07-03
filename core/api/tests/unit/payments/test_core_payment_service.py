import httpretty


from django.conf import settings
from api.tests.base import BaseAPITestCase
from api.services import CorePaymentProviderService
from api.services import OrderService, CartService

from api.tests.mocks.payments.razorpay import MockRazorPayRequests

class CorePaymentProviderServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product1 = self.make_model("Product", inventory_count=10, price=100)
        self.product2 = self.make_model("Product", inventory_count=10, price=100)
        self.buyer_address = self.make_model("BuyerAddress", user=self.user)

    @httpretty.activate
    def test_create_payment_request(self):
        # mock payment creation response from razorpay
        MockRazorPayRequests().mock_razorpay_requests()

        # add product1 to the cart
        CartService.add_to_cart(user=self.user, product_id=self.product1.id, quantity=1)
        user_cart = CartService.get_user_cart(user=self.user)
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart[0].quantity, 1)

        # create order for the user cart
        order = OrderService.create_order_from_cart(user=self.user)
        user_orders = OrderService.get_user_orders(user=self.user)
        self.assertEqual(user_orders.count(), 1)

        # create payment request
        payment_request_data = CorePaymentProviderService(
            payment_provider=OrderService.ORDER_PAYMENT_SERVICE_PROVIDER
        ).create_payment_request(
            total_amount=order.total_amount,
            order_id=order.id,
            currency="INR",
            additional_data={
                "order_id": order.id,
                "user_id": order.user.id,
            },
        )

        self.assertTrue(hasattr(payment_request_data, "url"))
