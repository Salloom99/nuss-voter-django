from django.contrib.auth.backends import BaseBackend
from .decryptor import decrypt
from rest_framework.authentication import BaseAuthentication

class QRBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        print(request)
        print(kwargs)
        # qr_encrypted = request.header.get('Authorization')
        # print(qr_encrypted)
        # try:
            # qr_id = decrypt(qr_encrypted)
        # except:
            # return
        # print(qr_id)
        # return qr_id

    def get_user(self, user_id):
        print(user_id)
        return None

    def get_user_permissions(self, user_obj, obj=None):
        return set()

    def get_group_permissions(self, user_obj, obj=None):
        return set()

    def get_all_permissions(self, user_obj, obj=None):
        return {
            *self.get_user_permissions(user_obj, obj=obj),
            *self.get_group_permissions(user_obj, obj=obj),
        }

    def has_perm(self, user_obj, perm, obj=None):
        print(perm)
        print(user_obj)
        return True
        # return perm in self.get_all_permissions(user_obj, obj=obj)
