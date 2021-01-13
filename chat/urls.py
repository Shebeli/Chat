from django.db.models import base
from django.urls.conf import include, path
from rest_framework import urlpatterns
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('private_chat', views.PCViewSet, basename='pc')
router.register('private_message', views.PCMViewSet, basename='pcm')
router.register('group', views.GroupViewSet, basename='group')
router.register('group_message', views.GCMViewSet, basename='gcm')
urlpatterns = [
    path('',include(router.urls))
]