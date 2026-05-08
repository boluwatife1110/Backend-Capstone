from django.db import models
from django.conf import settings
from listings.models import Listing


User = settings.AUTH_USER_MODEL

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('buy', 'Buy'),
        ('rent', 'Rent'),
    )

    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('declined', 'Declined'),
    )

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    transaction_type = models.CharField(max_length=10,choices=TRANSACTION_TYPE,default="buy")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.status}"