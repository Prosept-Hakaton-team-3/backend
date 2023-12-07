from django.contrib.auth.models import AbstractUser

from config.constants import TEXT_VIEW_SIZE


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:TEXT_VIEW_SIZE]
