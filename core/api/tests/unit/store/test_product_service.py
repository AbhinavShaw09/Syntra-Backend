from api.tests.base import BaseAPITestCase
from api.services import ProductService


class ProductServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product1 = self.make_model("Product")
        self.product2 = self.make_model("Product")

    def test_get_all_store_product(self):
        products = list(ProductService.get_all_products())
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)

    def test_get_store_product_by_id(self):
        product = ProductService.get_product_by_id(self.product1.id)
        self.assertEqual(product, self.product1)

    def test_check_product_availability(self):
        is_available = ProductService.check_product_availability(
            product_id=self.product1.id, quantity=10
        )
        self.assertEqual(is_available, False)

        self.product1.inventory_count = 10
        self.product1.save()

        is_available = ProductService.check_product_availability(
            product_id=self.product1.id, quantity=10
        )
        self.assertEqual(is_available, True)
