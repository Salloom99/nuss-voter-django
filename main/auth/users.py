import json
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Unit, Voter, Department
# from .decryptor import decrypt


class VoterUser(AnonymousUser):

    def __init__(self, qr_id) -> None:
        self.id = qr_id
        qr_parts = qr_id.split('_')
        self.qr_id = qr_parts[-1]
        self.is_voter = True
        self.unit_nickname = '_'.join(qr_parts[:2])
        
    @property
    def is_authenticated(self):
        valid_unit = Unit.objects.filter(nickname=self.unit_nickname).exists()
        voter_exists =  Voter.objects.filter(qr_id=self.qr_id, unit=self.unit_nickname).exists()
        return valid_unit and not voter_exists

    def get_token(self):
        return RefreshToken.for_user(self).access_token

    @property
    def is_anonymous(self):
        return False

    def __str__(self) -> str:
        return self.id

    
class MonitorUser(AnonymousUser):

    def __init__(self, register_data) -> None:
        self.id = register_data['unit']
        self.is_staff = True
        self.password = register_data['password']
        self.department = register_data['department']

    @classmethod
    def from_body(cls, binary_data):
        raw_data = binary_data.decode('utf-8')
        register_data = json.loads(raw_data)
        return cls(register_data)


    def get_token(self):
        token = RefreshToken.for_user(self).access_token
        token['user_type'] = 'monitor'
        token['department'] = self.department
        token['password'] = self.password
        return token

    def response(self):
        if self.is_authenticated:
            return JsonResponse({'token': f'{self.get_token()}'})
        return JsonResponse({'detail': 'invalid password'}, status=401)

    @property
    def is_authenticated(self):
        return Department.objects.get(
            pk=self.department).password == self.password

    @property
    def is_anonymous(self):
        return False
    
    def __str__(self) -> str:
        return self.id

