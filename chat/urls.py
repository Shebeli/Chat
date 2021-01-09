from django.urls.conf import include, path
from rest_framework import urlpatterns
from .views import UserViewSet, PCViewSet, PCMViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('private_chat', PCViewSet, basename='pc')
router.register('private_message', PCMViewSet, basename='pcm')
urlpatterns = [
    path('',include(router.urls))
]