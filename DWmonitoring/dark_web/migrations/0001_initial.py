# Generated by Django 5.0.6 on 2024-06-20 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlackMarket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=255)),
                ('stealer_log_preview', models.TextField()),
                ('related_assets', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Sold', 'Sold'), ('Unavailable', 'Unavailable')], max_length=12)),
                ('obtain_progress', models.CharField(max_length=255)),
                ('discovery_date', models.DateField()),
                ('incident', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_bin_number', models.IntegerField(blank=True, null=True, verbose_name='Card BIN Number')),
                ('card_type', models.CharField(blank=True, max_length=40, null=True, verbose_name='Card Type')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Expiry Date')),
                ('cvv', models.IntegerField(blank=True, null=True, verbose_name='CVV')),
                ('card_holder_name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Card Holder Name')),
                ('issuing_bank', models.CharField(blank=True, max_length=255, null=True, verbose_name='Issuing Bank')),
                ('breach_date', models.DateField(blank=True, null=True, verbose_name='Breach Date')),
                ('posted_date', models.DateField(auto_now_add=True)),
                ('breach_source', models.CharField(max_length=255, verbose_name='Breach Source')),
                ('last_used_date', models.DateField(blank=True, null=True, verbose_name='Last Used Date')),
                ('breach_source_domain', models.CharField(blank=True, max_length=255, null=True, verbose_name='Breach Source Domain')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('domain_ip', models.GenericIPAddressField()),
                ('source_ip', models.GenericIPAddressField()),
                ('source_domain', models.TextField()),
                ('breach_date', models.DateField(blank=True, null=True)),
                ('posted_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PIIExposure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('breach_date', models.DateField(blank=True, null=True)),
                ('posted_date', models.DateField(auto_now_add=True)),
                ('breach_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('source_domain', models.CharField(blank=True, max_length=255, null=True)),
                ('threat_type', models.CharField(blank=True, max_length=255, null=True)),
                ('type_of_data', models.CharField(blank=True, max_length=255, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StealerLogs',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_detected', models.DateField()),
                ('data_type', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_title', models.CharField(blank=True, max_length=255, null=True)),
                ('ticket_description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ticket_images/')),
                ('resolved', models.BooleanField(default=False)),
            ],
        ),
    ]
