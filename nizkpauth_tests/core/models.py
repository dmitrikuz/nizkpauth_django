from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from nizkpauth_django.django.fields import NIZKPProfileField

class UserWithProfile(AbstractBaseUser):
    profile = NIZKPProfileField()
    user_id = models.CharField(max_length=60, unique=True)

    USERNAME_FIELD = "user_id"
