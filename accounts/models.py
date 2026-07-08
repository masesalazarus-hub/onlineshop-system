from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )

    def __str__(self):
        return self.user.username