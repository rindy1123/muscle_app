from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    user_vali = UnicodeUsernameValidator()
    username = models.CharField(_('username'), max_length=150, unique=True, validators=[user_vali])
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0)
    email = models.EmailField(_('email address'), unique=True)
    workoutdegree = models.FloatField(default=0)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']