from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Unit, Voter, Department
# from .decryptor import decrypt

class VoterUser(AnonymousUser):

    def __init__(self, qr_id) -> None:
        self.id = qr_id
        qr_parts = qr_id.split('_')
        self.username = qr_parts[-1]
        self.unit_nickname = '_'.join(qr_parts[:2])
        self.authenticated = Unit.objects.filter(nickname=self.unit_nickname).exists() \
            and not Voter.objects.filter(qr_id=self.username, unit=self.unit_nickname).exists()
        self.token = RefreshToken.for_user(self).access_token

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False



class MonitorUser(AnonymousUser):

    def __init__(self, register_data) -> None:
        self.id = register_data['unit']
        self.authenticated = Department.objects.get(pk=register_data['department']).password == register_data['password']
        self.authenticated = True
        self.token = RefreshToken.for_user(self).access_token

    @classmethod
    def get(cls, unit):
        user = type(f'{cls}',(object,),{"id": unit, 'is_authenticated': True})()
        user.token = RefreshToken.for_user(user).access_token
        return user

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False
