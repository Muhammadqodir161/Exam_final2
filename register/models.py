from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(5)], verbose_name=_('Name'))
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=_('Avatar'))
    email_verified = models.BooleanField(default=False, verbose_name=_('Email Verified'))

    def __str__(self):
        return self.username


