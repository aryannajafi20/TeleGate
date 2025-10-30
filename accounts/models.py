from django.db import models
from django.contrib.auth.models import AbstractBaseUser as AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have a email')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_developer = True
        user.save(using=self._db)
        return user



class User(AbstractUser):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
        return True
    def __str__(self):
        return str(self.username)

    @property
    def is_staff(self):
        return self.is_developer