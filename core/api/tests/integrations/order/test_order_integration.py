from rest_framework import status
from api.tests.base import BaseAPITestCase
from api.models import Order, CartItem


class OrderIntegrationTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        # Create cart items for testing
        self.cart_item = CartItem.objects.create(
            user=self.user, product=self.product1, quantity=2
        )

    def test_buyer_create_and_seller_view_order(self):
        """Test buyer creates order and seller can view it"""
        # Buyer creates order
        response = self.auth_client.post("/api/buyer/order/")

        self.assertSuccessReponse(response)
        order_id = response.data["id"]

        # Buyer can retrieve their order
        response = self.auth_client.get(f"/api/buyer/order/{order_id}/")
        self.assertSuccessReponse(response)

        # Seller can view order in their list
        response = self.auth_client.get("/api/seller/orders/")
        self.assertSuccessReponse(response)
        order_ids = [order["id"] for order in response.data]
        self.assertIn(order_id, order_ids)

    def test_buyer_list_orders(self):
        """Test buyer can list their orders"""
        # Create order via buyer endpoint
        self.auth_client.post("/api/buyer/order/")

        # List orders via buyer endpoint
        response = self.auth_client.get("/api/buyer/order/")

        self.assertSuccessReponse(response)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    def test_seller_update_order_status(self):
        """Test seller can update order status"""
        # Create order
        response = self.auth_client.post("/api/buyer/order/")
        order_id = response.data["id"]

        # Seller updates order status
        payload = {"status": Order.StatusChoices.SHIPPED}
        response = self.auth_client.put(f"/api/seller/orders/{order_id}/", payload)

        self.assertSuccessReponse(response)

        # Buyer sees updated status
        response = self.auth_client.get(f"/api/buyer/order/{order_id}/")
        self.assertSuccessReponse(response)
        self.assertEqual(response.data["status"], "Shipped")

    def test_seller_all_orders_endpoint(self):
        """Test seller can view all orders"""
        # Create multiple orders
        self.auth_client.post("/api/buyer/order/")

        # Add more items to cart and create another order
        CartItem.objects.create(user=self.user, product=self.product1, quantity=1)
        self.auth_client.post("/api/buyer/order/")

        # Seller views all orders
        response = self.auth_client.get("/api/seller/orders/all/")

        self.assertSuccessReponse(response)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 2)
