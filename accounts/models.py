
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('store_manager', 'Store Manager'),
        ('employee', 'Employee'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='employee')

    def __str__(self):
        return self.username

    def get_store(self):
        try:
            return self.storeemployee_set.first().store
        except AttributeError:
            return None

    get_store.short_description = 'Store'

    def save(self, *args, **kwargs):
        if self.is_superuser and self.user_type != 'admin':
            self.user_type = 'admin'
        super().save(*args, **kwargs)