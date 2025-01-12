from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field

class User(AbstractUser):
    bio = CKEditor5Field(
        config_name='default',
        blank=True
    )

    def __str__(self):
        return f"{self.username}"