from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_mail_with_template(sender, instance, created, **kwargs):
      if created:
         send_mail(
             subject='Welcome to Our App',
             message=f'Hi {instance.first_name}, welcome to our app!',
             from_email='woruboluwatife11@gmail.com',
             recipient_list=[instance.email],
             fail_silently=False,
         )