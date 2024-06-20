from django.contrib import admin
from .models import Card,BlackMarket,Domain,PIIExposure,StealerLogs, Notification, Ticket

# Register your models here.
admin.site.register(Card)
admin.site.register(BlackMarket)
admin.site.register(Domain)
admin.site.register(PIIExposure)
admin.site.register(StealerLogs)
admin.site.register(Notification)
admin.site.register(Ticket)