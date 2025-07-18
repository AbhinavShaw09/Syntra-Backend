from api.tests.base import BaseAPITestCase
from api.services import BuyerAccountDetailsService


class BuyerAccountDetailsServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()

    def test_get_buyer_addresses(self):
        buyer_details = BuyerAccountDetailsService.get_all_buyer_details(
            user_id=self.user.id
        )
        self.assertIsNotNone(buyer_details)
        self.assertEqual(buyer_details.id, self.user.id)
        self.assertEqual(buyer_details.email, self.user.email)
        self.assertEqual(buyer_details.username, self.user.username)
