from api.tests.base import BaseAPITestCase
from api.services import BuyerAddressService
from api.models import BuyerAddress


class BuyerAddressServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()

    def test_get_buyer_addresses(self):
        buyer_addresses = BuyerAddressService.get_all_buyer_address(
            user_id=self.user.id
        )
        self.assertEqual(buyer_addresses.count(), 1)

        buyer_address = self.make_model(BuyerAddress, user_id=self.user.id)
        self.assertIsInstance(buyer_address, BuyerAddress)

        buyer_addresses = BuyerAddressService.get_all_buyer_address(
            user_id=self.user.id
        )
        self.assertEqual(buyer_addresses.count(), 2)
