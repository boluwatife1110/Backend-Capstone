from rest_framework import generics, permissions
from .models import Transaction
from rest_framework import serializers
from .serializers import TransactionSerializer
from listings.models import Listing
from properties.permissions import IsSellerOrAgent


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

   

    def perform_create(self, serializer):
        listing_id = self.request.data.get("listing")
        listing_obj = Listing.objects.get(id=listing_id)

        
        if listing_obj.seller == self.request.user:
            raise serializers.ValidationError("You cannot buy your own property.")

        serializer.save(
            buyer=self.request.user,
            seller=listing_obj.property.seller,
            amount=listing_obj.price
        )

class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsSellerOrAgent]