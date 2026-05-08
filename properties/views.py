from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Property
from .serializers import PropertySerializer
from .permissions import IsSellerOrAgent

# List all properties or create a new one
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsSellerOrAgent]  # Only logged-in users can create

    def perform_create(self, serializer):
        # Save the property with the current user as seller
        serializer.save(seller=self.request.user)


# Retrieve, update, or delete a specific property
class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsSellerOrAgent]


    def perform_update(self, serializer):
        # Only the seller can update their property
        if serializer.instance.seller != self.request.user:
            raise PermissionDenied("You do not have permission to update this property.")
        serializer.save()

    def perform_destroy(self, instance):
        # Only the seller can delete their property
        if instance.seller != self.request.user:
            raise PermissionDenied("You do not have permission to delete this property.")
        instance.delete()

    