from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from djpgv.core.models import BaseModel


class UserManager(BUM):
    def create_user(self, email: str, password: str, is_superuser: bool = False):
        user = self.model(email=self.normalize_email(email.lower()), is_superuser=is_superuser)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password, is_superuser=True)
        user.save(using=self._db)

        return user

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing
        """
        email = email or ""

        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name.lower() + "@" + domain_part.lower()

        return email


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_superuser

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
