from django.contrib import admin

from .models import Event, TelegramUser


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date_time', 'location')


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'subscribed')
    search_fields = ('user_id', 'username', 'first_name', 'last_name')
    list_filter = ('subscribed',)
