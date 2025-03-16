import os
from dotenv import load_dotenv
from rest_framework.permissions import BasePermission


load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')


class AllowTelegramOrAuthenticated(BasePermission):
    """
    Разрешает доступ только для Telegram бота или аутентифицированных пользователей.
    """
    def has_permission(self, request, view):

        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            bot_token = request.headers.get('Bot-Token')
            allowed_bot_token = BOT_TOKEN
            return bot_token == allowed_bot_token
                
        return request.user.is_authenticated or request.headers.get('Bot-Token') == BOT_TOKEN
