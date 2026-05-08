from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.


class User(AbstractUser):
    USER_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
         ('agent', 'Agent'),

    )
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    user_type = models.CharField(max_length=10,choices=USER_CHOICES,default='buyer')
    first_name = models.CharField(max_length=40, blank=True, null=True) 
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False ) 
    phone_number = models.CharField(max_length=15, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'phone_number']

    objects = UserManager()