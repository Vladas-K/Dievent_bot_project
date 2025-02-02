from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    company_info = models.TextField()
    dress_code = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class TelegramUser(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.username if self.username else str(self.user_id)
