from aifc import Error
# from rest_framework import authentication, exceptions, settings
# from rest_framework.authentication import get_authorization_header
from .voter import VoterUser

from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.authentication import api_settings


class VoterAuthentication(authentication.JWTAuthentication):
    # keyword = 'Token'

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
       
        qr_id = validated_token[api_settings.USER_ID_CLAIM]       
        return VoterUser(qr_id)
        
