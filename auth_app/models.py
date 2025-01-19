from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


class AttributeAccessControl(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="attributes")
    department = models.CharField(max_length=100, blank=True, null=True)
    geographic_location = models.CharField(max_length=100, blank=True, null=True)
    account_status = models.CharField(
        max_length=50,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
    )

    def __str__(self):
        return f"Attributes of {self.user.username}"