from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from main import serializers
from main.auth.users import VoterUser, MonitorUser
from main.auth.permissions import FinishedUnit, IsVoter
from .models import Department, Unit, Nominee, Voter
from .auth.decryptor import encrypt, decrypt


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerilaizer


class UnitViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'options']
    queryset = Unit.objects.all()
    filterset_fields = ['department']

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [FinishedUnit(), IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.UpdateUnitStateSerializer
        return serializers.UnitSerilaizer


class NomineeViewSet(ModelViewSet):
    queryset = Nominee.objects.annotate(votes_count=Count('votes'))
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['unit']
    ordering_fields = ['name', 'votes_count']

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.UpdateNomineeSerializer
        return serializers.NomineeSerilaizer

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class VoterViewSet( mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Voter.objects.select_related('unit').prefetch_related('votes')
    filter_backends = [DjangoFilterBackend]
    # filterset_class = VoterFilter
    filterset_fields = ['unit']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsVoter()]        
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateVoterSerializer
        return serializers.VoterSerilaizer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path= r'total-in/(?P<unit>\w+)'
    )
    def get_total_votes(self, request, unit):
        votes_count = Voter.objects.filter(unit=unit).aggregate(Count('pk'))
        return Response({ 'total_votes':votes_count['pk__count']})


@api_view(['POST'])
def monitor_register(request):
    user = MonitorUser.from_body(request.body)
    return user.response()

@api_view(['GET'])
def get_token(request, qr_id):
    user = VoterUser(qr_id)
    return Response({ 'token': f'{user.get_token()}' })

def say_hello(request):
    if request.user.is_authenticated:
        return HttpResponse(f'<h1>You don\'t have permission to say hello</h1>')
    # name = decrypt(name) if len(name) > 10 else encrypt(name)
    return HttpResponse(f'<h1>Hello!</h1>')

