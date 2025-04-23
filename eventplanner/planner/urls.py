from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, TelegramUserViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', TelegramUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
