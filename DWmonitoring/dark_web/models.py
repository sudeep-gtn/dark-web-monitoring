from django.db import models

class Card(models.Model):
    card_bin_number = models.IntegerField(null=True, blank=True, verbose_name='Card BIN Number')
    card_type = models.CharField(max_length=40, null=True, blank=True, verbose_name='Card Type')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='Expiry Date')
    cvv = models.IntegerField(null=True, blank=True, verbose_name='CVV')
    card_holder_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='Card Holder Name')
    issuing_bank = models.CharField(max_length=255, null=True, blank=True, verbose_name='Issuing Bank')
    breach_date = models.DateField(null=True, blank=True, verbose_name='Breach Date')
    breach_source = models.CharField(max_length=255, verbose_name='Breach Source')
    last_used_date = models.DateField(null=True, blank=True, verbose_name='Last Used Date')
    SEVERITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    severity_level = models.CharField(max_length=10, choices=SEVERITY_CHOICES, verbose_name='Severity Level', default='Low')
    breach_source_domain = models.CharField(max_length=255, null=True, blank=True, verbose_name="Breach Source Domain")