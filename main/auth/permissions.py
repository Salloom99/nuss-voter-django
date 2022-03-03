from rest_framework.permissions import BasePermission
from main.models import Unit


class IsVoter(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_voter)


class FinishedUnit(BasePermission):
    def has_permission(self, request, view):
        unit = view.kwargs['pk']
        unit_state = Unit.objects.get(pk=unit).state
        if unit_state == 'F':
            return False
        return True
