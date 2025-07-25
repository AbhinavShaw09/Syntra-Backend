from api.tests.base import BaseAPITestCase


class SellerProductCategoriesIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.get_auth_client()
        self.product2 = self.make_model("Product")
        self.product3 = self.make_model("Product")
        self.product_category1 = self.make_model("ProductCategory")
        self.product_category2 = self.make_model("ProductCategory")

    def get_product_caetgory_payload(self):
        return {
            "name": self.product_category1.name,
        }

    def test_seller_list_product_categories(self):
        response = self.client.get(
            path="/api/seller/categories/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 2)

    def test_seller_create_product_category(self):
        response = self.client.post(
            path=f"/api/seller/categories/",
            data=self.get_product_caetgory_payload(),
            content_type="application/json",
        )
        self.assertSuccessReponse(response)

    def test_seller_patch_product_categories(self):
        patch_payload = {
            "name": "test_name",
        }
        response = self.client.patch(
            path=f"/api/seller/categories/{self.product_category1.id}/",
            data=patch_payload,
            content_type="application/json",
        )
        self.assertSuccessReponse(response)

        self.assertEqual(response.data["name"], "test_name")

    def test_seller_delete_product_categories(self):
        response = self.client.post(
            path=f"/api/seller/categories/{self.product_category1.id}/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
