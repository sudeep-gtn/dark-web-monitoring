from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Card, Domain, BlackMarket, StealerLogs, PIIExposure, Notification

@receiver(post_save, sender=Card)
def create_card_notification(sender, instance, created, **kwargs):
    if created:
        message = f"A new card breach has been detected : {instance.card_bin_number}"
        Notification.objects.create(message=message)

@receiver(post_save, sender=Domain)
def create_domain_notification(sender, instance, created, **kwargs):
    if created:
        message = f"A new domain breach has been detected: {instance.name}"
        Notification.objects.create(message=message)

@receiver(post_save, sender=BlackMarket)
def create_blackmarket_notification(sender, instance, created, **kwargs):
    if created:
        message = f"A new black market entry has been detected : {instance.source}"
        Notification.objects.create(message=message)

@receiver(post_save, sender=StealerLogs)
def create_stealerlogs_notification(sender, instance, created, **kwargs):
    if created:
        message = f"A new stealer log has been detected : {instance.log_id}"
        Notification.objects.create(message=message)

@receiver(post_save, sender=PIIExposure)
def create_piiexposure_notification(sender, instance, created, **kwargs):
    if created:
        message = f"A new PII exposure has been detected : {instance.name}"
        Notification.objects.create(message=message)
