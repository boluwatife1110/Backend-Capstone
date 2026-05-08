from django.urls import path
from users import views



urlpatterns =[
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path("logout/", views.logout, name='logout'),
]