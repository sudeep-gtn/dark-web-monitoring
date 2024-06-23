import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import string


def generate_otp():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))


def send_otp_email(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save()
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. It is valid for 10 minutes.'
    send_mail(subject, message, 'from@example.com', [user.email])


def is_otp_valid(user, otp):
    if user.otp == (
        otp and timezone.now() < user.otp_created_at + timedelta(minutes=10)
    ):
        return True
    return False
