from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import say_hello, DepartmentViewSet, UnitViewSet, NomineeViewSet, VoterViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'nominees', NomineeViewSet, basename='nominee')
router.register(r'voters', VoterViewSet, basename='voter')

urlpatterns = [
    path('hello/', say_hello),
    *router.urls
]
