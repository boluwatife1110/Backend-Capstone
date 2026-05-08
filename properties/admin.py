from django.contrib import admin
from .models import Property

@admin.register(Property)
class CustomPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'preview_image', 'seller', 'title','description','location')
    search_fields = ('id','preview_image', 'title', 'seller', 'description', 'location')