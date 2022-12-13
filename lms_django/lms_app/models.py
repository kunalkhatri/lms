from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username        = None
    email           = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects         = UserManager()

class className(models.Model):
    name            = models.CharField(max_length=100)
    active          = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class classStartTime(models.Model):
    time            = models.TimeField(verbose_name="Class Start Time")

    def __str__(self) -> str:
        return str(self.time)

class attendance(models.Model):
    lecturer        = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    classname       = models.ForeignKey(className,on_delete=models.DO_NOTHING)
    class_start_time= models.ForeignKey(classStartTime,on_delete=models.DO_NOTHING)
    date            = models.DateField(default=timezone.now)
    headcount       = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.classname} | {self.class_start_time} | {self.headcount} "

