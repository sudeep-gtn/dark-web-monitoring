from django.db import models

class Card(models.Model):
    card_bin_number = models.IntegerField(null=True, blank=True, verbose_name='Card BIN Number')
    card_type = models.CharField(max_length=40, null=True, blank=True, verbose_name='Card Type')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='Expiry Date')
    cvv = models.IntegerField(null=True, blank=True, verbose_name='CVV')
    card_holder_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='Card Holder Name')
    issuing_bank = models.CharField(max_length=255, null=True, blank=True, verbose_name='Issuing Bank')
    breach_date = models.DateField(null=True, blank=True, verbose_name='Breach Date')
    posted_date = models.DateField(auto_now_add=True)
    
    breach_source = models.CharField(max_length=255, verbose_name='Breach Source')
    last_used_date = models.DateField(null=True, blank=True, verbose_name='Last Used Date')
    breach_source_domain = models.CharField(max_length=255, null=True, blank=True, verbose_name="Breach Source Domain")

    def __str__(self):
        return str(self.card_bin_number)
    
class Domain(models.Model):
    name = models.CharField(max_length=255)
    domain_ip = models.GenericIPAddressField()
    source_ip = models.GenericIPAddressField()
    source_domain = models.TextField()
    breach_date = models.DateField(null=True, blank=True)
    posted_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.name} - {self.domain_ip}'

class BlackMarket(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Unavailable', 'Unavailable'),
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
    name = models.CharField(max_length=255, null=True, blank=True)
    breach_date = models.DateField(null=True, blank=True)
    posted_date = models.DateField(auto_now_add=True)
    breach_ip = models.GenericIPAddressField(null=True, blank=True)
    source_domain = models.CharField(max_length=255, null=True, blank=True)
    threat_type = models.CharField(max_length=255, null=True, blank=True)
    type_of_data = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.breach_ip} - {self.breach_date}'
    
def calculate_organization_health():
    """Calculates the overall organization health status (1-100)."""
    # Returning a static value
    return 50

class Notification(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_title = models.CharField(max_length=255, null=True, blank=True)
    ticket_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='ticket_images/', blank=True, null=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.ticket_title
