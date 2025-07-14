from api.tests.base import BaseAPITestCase


class CartIntegrationsTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.get_auth_client()
        self.product1 = self.make_model("Product", inventory_count=10)

    def get_buyer_cart_payload(self):
        return {"product": str(self.product1.id), "quantity": 5}

    def create_buyer_cart(self):
        return self.client.post(
            "/api/buyer/cart/",
            data=self.get_buyer_cart_payload(),
            content_type="application/json",
        )

    def test_seller_cart_list_products(self):
        response = self.client.get(
            path="/api/buyer/cart/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 0)

        response = self.create_buyer_cart()
        self.assertSuccessReponse(response)

        response = self.client.get(
            path="/api/buyer/cart/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 1)

    def test_seller_cart_partial_update_products(self):
        response = self.create_buyer_cart()
        self.assertSuccessReponse(response)

        response = self.client.get(
            path="/api/buyer/cart/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 1)

        response = self.client.patch(
            path=f"/api/buyer/cart/{str(self.product1.id)}/",
            data={"quantity": 3},
            content_type="application/json",
        )

        self.assertSuccessReponse(response)
        self.assertEqual(response.json().get("quantity"), 3)

    def test_seller_cart_delete_products(self):
        response = self.create_buyer_cart()
        self.assertSuccessReponse(response)

        response = self.client.get(
            path="/api/buyer/cart/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 1)

        response = self.client.delete(
            path=f"/api/buyer/cart/{str(self.product1.id)}/",
            content_type="application/json",
        )

        self.assertSuccessReponse(response)

        response = self.client.get(
            path="/api/buyer/cart/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 0)
