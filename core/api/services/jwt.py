from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Seller, Buyer


class JwtService:
    def __init__(self, user: User):
        self.user = user

    def get_token(self) -> RefreshToken:
        if not User.objects.filter(id=self.user.id).exists():
            raise ValueError("User does not exist")

        user = self.user
        seller = Seller.objects.get_or_create(
            user=user, name=user.username, email=user.email
        )[0]
        buyer = Buyer.objects.get_or_create(
            user=user, name=user.username, email=user.email
        )[0]

        token: RefreshToken = RefreshToken.for_user(self.user)
        token["name"] = self.user.username
        token["email"] = self.user.email
        token["phone"] = seller.phone
        token["seller_id"] = seller.id
        token["buyer_id"] = buyer.id

        return token
