from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import UserLoginHistory

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLoginHistory.objects.create(
        user=user,
        ip_address=request.META.get('REMOTE_ADDR'),
        timestamp=timezone.now()
    )
