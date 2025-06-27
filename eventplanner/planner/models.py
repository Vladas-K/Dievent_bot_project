from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание мероприятия")
    date_time = models.DateTimeField(verbose_name="Дата проведения")
    location = models.TextField(verbose_name="Место проведения")
    company_info = models.TextField(verbose_name="Информация о компании организаторе")
    dress_code = models.CharField(
        max_length=200, verbose_name="Дресс-код"
    )

    class Meta:
        verbose_name = "объект «Мероприятие»"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title


class TelegramUser(models.Model):
    user_id = models.CharField(max_length=50, unique=True, verbose_name="id")
    username = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Юзернейм"
    )
    first_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Фамилия"
    )
    subscribed = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = 'объект "Пользователь Telegram"'
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return self.username if self.username else str(self.user_id)
