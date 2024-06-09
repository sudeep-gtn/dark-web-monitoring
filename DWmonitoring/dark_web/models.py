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





class Domain(models.Model):
    SEVERITY_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    name = models.CharField(max_length=255)
    domain_ip = models.GenericIPAddressField()
    severity_level = models.CharField(max_length=6, choices=SEVERITY_LEVEL_CHOICES)
    source_ip = models.GenericIPAddressField()
    source_domain = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.ip}'
    

class BlackMarket(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('unavailable', 'Unavailable'),
    ]
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=255)
    stealer_log_preview = models.TextField()
    related_assets = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    obtain_progress = models.CharField(max_length=255)
    discovery_date = models.DateField()
    incident = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.source} - {self.status}'
    
class StealerLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    date_detected = models.DateField()
    data_type = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return f'Log {self.log_id} - {self.date_detected}'

class PIIExposure(models.Model):
    SEVERITY_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    name = models.CharField(max_length=255)
    breach_date = models.DateField()
    breach_ip = models.GenericIPAddressField()
    domain = models.CharField(max_length=255)
    threat_type = models.CharField(max_length=255)
    severity_level = models.CharField(max_length=6, choices=SEVERITY_LEVEL_CHOICES)
    type_of_data = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    personal_email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} - {self.breach_ip} - {self.breach_date}'