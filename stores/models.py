

# Create your models here.
from django.db import models
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_store'
    )

    def __str__(self):
        return self.name

# Add this new model to create the many-to-many relationship
class StoreEmployee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'store')