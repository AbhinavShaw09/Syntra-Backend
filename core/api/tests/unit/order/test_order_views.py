from rest_framework import status
from api.tests.base import BaseAPITestCase
from api.models import Order, OrderItem, CartItem


class OrderViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        # Create cart items for testing
        self.cart_item = CartItem.objects.create(
            user=self.user, product=self.product1, quantity=2
        )

    def test_create_order_success(self):
        """Test creating order from cart"""
        response = self.auth_client.post("/api/seller/orders/")

        self.assertSuccessReponse(response)
        self.assertIn("id", response.data)
        self.assertIn("total_amount", response.data)
        self.assertIn("status", response.data)
        self.assertIn("items", response.data)

        # Verify order exists in database
        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.user, self.user)

    def test_create_order_empty_cart(self):
        """Test creating order with empty cart fails"""
        CartItem.objects.filter(user=self.user).delete()

        response = self.auth_client.post("/api/seller/orders/")

        self.assertErrorResponse(response)

    def test_list_user_orders(self):
        """Test listing user's orders"""
        # Create an order first
        order = self.make_model("Order", user=self.user, total_amount=100.00)

        response = self.auth_client.get("/api/seller/orders/")

        self.assertSuccessReponse(response)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], order.id)

    def test_retrieve_order_success(self):
        """Test retrieving specific order"""
        order = self.make_model("Order", user=self.user, total_amount=100.00)

        response = self.auth_client.get(f"/api/seller/orders/{order.id}/")

        self.assertSuccessReponse(response)
        self.assertEqual(response.data["id"], order.id)
        self.assertEqual(float(response.data["total_amount"]), 100.00)

    def test_retrieve_order_not_found(self):
        """Test retrieving non-existent order"""
        response = self.auth_client.get("/api/seller/orders/99999/")

        self.assertErrorResponse(response)

    def test_retrieve_other_user_order(self):
        """Test user cannot retrieve another user's order"""
        other_user = self.make_model("User")
        order = self.make_model("Order", user=other_user, total_amount=100.00)

        response = self.auth_client.get(f"/api/seller/orders/{order.id}/")

        self.assertErrorResponse(response)

    def test_update_order_status_success(self):
        """Test updating order status"""
        order = self.make_model("Order", user=self.user, total_amount=100.00)

        payload = {"status": Order.StatusChoices.SHIPPED}
        response = self.auth_client.put(f"/api/seller/orders/{order.id}/", payload)

        self.assertSuccessReponse(response)

        # Verify status updated in database
        order.refresh_from_db()
        self.assertEqual(order.status, Order.StatusChoices.SHIPPED)

    def test_update_order_status_invalid(self):
        """Test updating order with invalid status"""
        order = self.make_model("Order", user=self.user, total_amount=100.00)

        payload = {"status": 999}
        response = self.auth_client.put(f"/api/seller/orders/{order.id}/", payload)

        self.assertErrorResponse(response)

    def test_get_all_seller_orders(self):
        """Test getting all seller orders"""
        order1 = self.make_model("Order", user=self.user, total_amount=100.00)
        order2 = self.make_model("Order", user=self.user, total_amount=200.00)

        response = self.auth_client.get("/api/seller/orders/all/")

        self.assertSuccessReponse(response)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 2)

    def test_unauthorized_access(self):
        """Test unauthorized access to orders"""
        response = self.client.get("/api/seller/orders/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_with_items_serialization(self):
        """Test order serialization includes items"""
        order = self.make_model("Order", user=self.user, total_amount=100.00)
        order_item = self.make_model(
            "OrderItem",
            order=order,
            product=self.product1,
            quantity=2,
            unit_price=50.00,
        )

        response = self.auth_client.get(f"/api/seller/orders/{order.id}/")

        self.assertSuccessReponse(response)
        self.assertIn("items", response.data)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["quantity"], 2)
        self.assertEqual(float(response.data["items"][0]["unit_price"]), 50.00)
