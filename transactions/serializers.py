from rest_framework import serializers
from .models import Transaction



class TransactionSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source="buyer.username")
    seller = serializers.ReadOnlyField(source="seller.username")

    class Meta:
        model = Transaction
        fields = "__all__"


    def validate(self, data):
     listing = data.get('listing')
     amount = data.get('amount')

     if listing and amount:
        if amount != listing.price:
            data['status'] = 'Declined'
        else:
            data['status'] = 'Confirmed'

     return data

        