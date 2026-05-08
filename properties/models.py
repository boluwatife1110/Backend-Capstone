from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Property(models.Model):
    preview_image = models.ImageField(default='houseimage.png', blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=250)

    def __str__(self):
        return self.title