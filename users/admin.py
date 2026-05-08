from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name','user_type', 'phone_number','profile_image')
    search_fields = ('id', 'email', 'first_name', 'last_name')

     
