from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):

    @property
    def is_system_admin(self):
        return self.groups.filter(name=settings.SYSTEM_ADMIN_GROUP).exists()

