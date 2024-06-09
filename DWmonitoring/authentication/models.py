from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email, full_name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


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