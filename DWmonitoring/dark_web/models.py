from django.db import models
from django.db.models import Avg

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

    def __str__(self):
        return str(self.card_bin_number)

    def get_severity_score(self):
        mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        return mapping.get(self.severity_level, 1) 

class Domain(models.Model):
    SEVERITY_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    name = models.CharField(max_length=255)
    domain_ip = models.GenericIPAddressField()
    severity_level = models.CharField(max_length=6, choices=SEVERITY_LEVEL_CHOICES)
    source_ip = models.GenericIPAddressField()
    source_domain = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.domain_ip}'
    
    def get_severity_score(self):
        mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        return mapping.get(self.severity_level, 1) 
    

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
    SEVERITY_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    name = models.CharField(max_length=255, null=True, blank=True)
    breach_date = models.DateField(null=True, blank=True)
    breach_ip = models.GenericIPAddressField(null=True, blank=True)
    source_domain = models.CharField(max_length=255, null=True, blank=True)
    threat_type = models.CharField(max_length=255, null=True, blank=True)
    severity_level = models.CharField(max_length=6, choices=SEVERITY_LEVEL_CHOICES)
    type_of_data = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.breach_ip} - {self.breach_date}'
    
    def get_severity_score(self):
        """Returns a numerical severity score for the PII exposure instance."""
        mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        return mapping.get(self.severity_level, 1)
    
def calculate_organization_health():
    """Calculates the overall organization health status (1-100)."""

    # Retrieve all instances of Card, Domain, and PIIExposure
    cards = Card.objects.all()
    domains = Domain.objects.all()
    piis = PIIExposure.objects.all()

    # Calculate average severity for each type
    avg_card_severity = sum(card.get_severity_score() for card in cards) / len(cards) if cards else 1
    avg_domain_severity = sum(domain.get_severity_score() for domain in domains) / len(domains) if domains else 1
    avg_pii_severity = sum(pii.get_severity_score() for pii in piis) / len(piis) if piis else 1

    # Weighted average calculation
    weighted_average = (
        (avg_card_severity * 0.4) +  # Card severity weighted at 40%
        (avg_domain_severity * 0.3) +  # Domain severity weighted at 30%
        (avg_pii_severity * 0.3)        # PII Exposure severity weighted at 30%
    )

    health_score = max(0, min(100, int((3 - weighted_average) / 2 * 100)))

    return health_score
