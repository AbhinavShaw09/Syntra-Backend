from rest_framework import status
from api.tests.base import BaseAPITestCase
from api.models import Product, ProductCategory, ProductCategoryMapping


class ProductCategoryMappingTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = self.make_model("ProductCategory", name="Electronics")
        self.category2 = self.make_model("ProductCategory", name="Books")

    def test_create_product_with_category(self):
        """Test creating a product with category_id creates mapping"""
        payload = {
            "name": "Test Product",
            "description": "Test Description",
            "original_price": "100.00",
            "selling_price": "90.00",
            "inventory_count": 10,
            "category_id": self.category.id
        }
        
        response = self.auth_client.post("/api/seller/products/create/", payload)
        
        self.assertSuccessReponse(response)
        self.assertEqual(response.data["name"], "Test Product")
        self.assertEqual(len(response.data["categories"]), 1)
        self.assertEqual(response.data["categories"][0]["id"], self.category.id)
        self.assertEqual(response.data["categories"][0]["name"], "Electronics")
        
        # Verify mapping exists in database
        product = Product.objects.get(id=response.data["id"])
        self.assertTrue(
            ProductCategoryMapping.objects.filter(
                product=product, category=self.category
            ).exists()
        )

    def test_create_product_without_category(self):
        """Test creating a product without category_id works"""
        payload = {
            "name": "Test Product",
            "description": "Test Description", 
            "original_price": "100.00",
            "selling_price": "90.00",
            "inventory_count": 10
        }
        
        response = self.auth_client.post("/api/seller/products/create/", payload)
        
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data["categories"]), 0)

    def test_create_product_with_invalid_category(self):
        """Test creating product with invalid category_id returns error"""
        payload = {
            "name": "Test Product",
            "description": "Test Description",
            "original_price": "100.00", 
            "selling_price": "90.00",
            "inventory_count": 10,
            "category_id": 99999
        }
        
        response = self.auth_client.post("/api/seller/products/create/", payload)
        
        self.assertErrorResponse(response)
        self.assertIn("category_id", response.data)

    def test_update_product_with_category(self):
        """Test updating product with category_id creates mapping"""
        product = self.make_model("Product", name="Original Product")
        
        payload = {"category_id": self.category.id}
        
        response = self.auth_client.patch(f"/api/seller/products/{product.id}/", payload)
        
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data["categories"]), 1)
        self.assertEqual(response.data["categories"][0]["id"], self.category.id)

    def test_seller_product_list_includes_categories(self):
        """Test seller product listing includes category information"""
        product = self.make_model("Product", name="Test Product")
        ProductCategoryMapping.objects.create(product=product, category=self.category)
        ProductCategoryMapping.objects.create(product=product, category=self.category2)
        
        response = self.auth_client.get("/api/seller/products/")
        
        self.assertSuccessReponse(response)
        
        # Find our test product in response
        test_product = next(
            (p for p in response.data if p["id"] == product.id), None
        )
        self.assertIsNotNone(test_product)
        self.assertEqual(len(test_product["categories"]), 2)
        
        category_names = [cat["name"] for cat in test_product["categories"]]
        self.assertIn("Electronics", category_names)
        self.assertIn("Books", category_names)

    def test_product_category_mapping_unique_constraint(self):
        """Test that duplicate product-category mappings are prevented"""
        product = self.make_model("Product")
        
        # Create first mapping
        mapping1 = ProductCategoryMapping.objects.create(
            product=product, category=self.category
        )
        
        # Try to create duplicate mapping
        with self.assertRaises(Exception):
            ProductCategoryMapping.objects.create(
                product=product, category=self.category
            )

    def test_multiple_products_same_category(self):
        """Test multiple products can belong to same category"""
        product1 = self.make_model("Product", name="Product 1")
        product2 = self.make_model("Product", name="Product 2")
        
        ProductCategoryMapping.objects.create(product=product1, category=self.category)
        ProductCategoryMapping.objects.create(product=product2, category=self.category)
        
        # Verify both mappings exist
        self.assertEqual(
            ProductCategoryMapping.objects.filter(category=self.category).count(), 2
        )

    def test_product_multiple_categories(self):
        """Test product can belong to multiple categories"""
        product = self.make_model("Product")
        
        ProductCategoryMapping.objects.create(product=product, category=self.category)
        ProductCategoryMapping.objects.create(product=product, category=self.category2)
        
        # Verify both mappings exist
        self.assertEqual(
            ProductCategoryMapping.objects.filter(product=product).count(), 2
        )
