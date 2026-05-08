from django.db import models
from properties.models import Property, User

# Create your models here.



class Listing(models.Model):
    LISTING_TYPE = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE) 
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE)
    
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.property.title} - {self.listing_type}"