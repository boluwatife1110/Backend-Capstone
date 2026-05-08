from rest_framework import generics
from .models import Listing
from .serializers import ListingSerializer
from rest_framework.exceptions import PermissionDenied
from .permissions import IsSellerOrAgent
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsSellerOrAgent]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().seller:
            raise PermissionDenied("You cannot edit this listing")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.seller:
            raise PermissionDenied("You cannot delete this listing")
        instance.delete()