import logging
from rest_framework import viewsets
from .models import Event, TelegramUser
from .serializers import EventSerializer, TelegramUserSerializer
from .permissions import AllowTelegramOrAuthenticated


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# class TelegramUserViewSet(viewsets.ModelViewSet):
#     queryset = TelegramUser.objects.all()
#     serializer_class = TelegramUserSerializer
#     permission_classes = [AllowTelegramOrAuthenticated]


logger = logging.getLogger(__name__)


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    permission_classes = [AllowTelegramOrAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if TelegramUser.objects.filter(user_id=user_id).exists():
            logger.warning(f"Пользователь с user_id {user_id} уже существует.")
        return super().create(request, *args, **kwargs)
