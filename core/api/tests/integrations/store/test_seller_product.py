from api.tests.base import BaseAPITestCase


class SellerProductIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.get_auth_client()
        self.product2 = self.make_model("Product")
        self.product3 = self.make_model("Product")

    def get_product_payload(self):
        return {
            "name": self.product1.name,
            "selling_price": self.product1.selling_price,
            "original_price": self.product1.original_price,
            "inventory_count": self.product1.inventory_count,
        }

    def test_seller_list_products(self):
        response = self.client.get(
            path="/api/seller/products/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 3)

    def test_seller_create_product(self):
        response = self.client.post(
            path=f"/api/seller/products/create/",
            data=self.get_product_payload(),
            content_type="application/json",
        )
        self.assertSuccessReponse(response)

    def test_seller_patch_product(self):
        patch_payload = {
            "inventory_count": 10,
        }
        response = self.client.patch(
            path=f"/api/seller/products/{self.product1.id}/",
            payload=patch_payload,
            content_type="application/json",
        )
        self.assertSuccessReponse(response)

        self.assertEqual(response.data["name"], self.product1.name)
        self.assertEqual(
            response.data["selling_price"], str(self.product1.selling_price)
        )
        self.assertEqual(
            response.data["original_price"], str(self.product1.original_price)
        )
        self.assertEqual(
            response.data["inventory_count"], self.product1.inventory_count
        )

    def test_seller_delete_product(self):
        response = self.client.delete(
            path=f"/api/seller/products/{self.product1.id}/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
