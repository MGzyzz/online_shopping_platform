from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    surname = models.CharField(max_length=50)
    phone = models.IntegerField()

    def __str__(self):
        return self.email
