from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'units', views.UnitViewSet, basename='unit')
router.register(r'nominees', views.NomineeViewSet, basename='nominee')
router.register(r'voters', views.VoterViewSet, basename='voter')

urlpatterns = [
    path('hello/', views.say_hello),
    path('register/', views.monitor_register),
    *router.urls
]
