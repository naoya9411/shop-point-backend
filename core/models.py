from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    user_email = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_email1',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    address_prefecture = models.CharField(max_length=10)
    address_city = models.CharField(max_length=20)
    hear_from = models.CharField(max_length=30)
    introduced = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name + self.first_name


class UserInfo(models.Model):

    user_email = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_email2',
        on_delete=models.CASCADE
    )
    point = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)
    continuous_visit_count = models.IntegerField(default=0, null=True)
    first_visit = models.DateTimeField(null=True)
    previous_visit = models.DateTimeField(null=True)
    last_visit = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_email)
