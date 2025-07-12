from api.tests.base import BaseAPITestCase


class ProductIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product1 = self.make_model("Product")
        self.product2 = self.make_model("Product")

    def test_get_all_products(self):
        response = self.client.get(path="/api/buyer/products/")
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_product(self):
        response = self.client.get(path=f"/api/buyer/products/{self.product1.id}/")
        self.assertSuccessReponse(response)
        response_data = response.json()
        self.assertEqual(response_data["id"], self.product1.id)
        self.assertEqual(response_data["name"], self.product1.name)
        self.assertEqual(
            response_data["original_price"], str(self.product1.original_price)
        )
        self.assertEqual(
            response_data["inventory_count"], self.product1.inventory_count
        )
