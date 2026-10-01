from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Users


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):

        user_id = validated_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed("User ID not found")

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return user