from pyexpat import model
from django_filters.rest_framework import FilterSet
from .models import Nominee, Voter

class NomineeFilter(FilterSet):
    class Meta:
        model = Nominee
        fields = {
            'unit__nickname': ['exact'],
        }

class VoterFilter(FilterSet):
    class Meta:
        model = Voter
        fields = {
            'unit__nickname': ['exact']
        }