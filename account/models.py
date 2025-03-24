from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email).lower()

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Permission(TimeStampedModel):
    title = models.CharField(max_length=100)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "permissions"
        ordering = ['-created_at']


class Role(TimeStampedModel):
    title = models.CharField(max_length=100)
    codename = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "roles"
        ordering = ['-created_at']


class User(AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(
        to=Role,
        related_name='users',
        on_delete=models.PROTECT,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

    def has_perm(self, perm):
        return self.role.permissions.filter(codename=perm).exists()
