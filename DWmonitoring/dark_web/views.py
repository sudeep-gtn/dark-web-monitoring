from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Card, Domain, BlackMarket, StealerLogs, PIIExposure, calculate_organization_health
import json
from django.db.models import Count
import requests
from collections import defaultdict

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        # Counts for all instances
        domains_count = Domain.objects.count()
        cards_count = Card.objects.count()
        pii_exposures_count = PIIExposure.objects.count()
        stealer_logs_count = StealerLogs.objects.count()

        # Severity counts for each model
        domain_severity_counts = Domain.objects.values('severity_level').annotate(count=Count('severity_level'))
        card_severity_counts = Card.objects.values('severity_level').annotate(count=Count('severity_level'))
        pii_exposure_severity_counts = PIIExposure.objects.values('severity_level').annotate(count=Count('severity_level'))

        # Organize severity counts into a dictionary
        severity_counts = {
            'domain': {level['severity_level']: level['count'] for level in domain_severity_counts},
            'card': {level['severity_level']: level['count'] for level in card_severity_counts},
            'pii_exposure': {level['severity_level']: level['count'] for level in pii_exposure_severity_counts},
        }

        # Ensure all severity levels are present in the dictionary
        for key in severity_counts:
            for level in ['Low', 'Medium', 'High']:
                if level not in severity_counts[key]:
                    severity_counts[key][level] = 0

        # Total severity counts for all models
        total_severity_counts = {
            'Low': sum(severity_counts[model].get('Low', 0) for model in severity_counts),
            'Medium': sum(severity_counts[model].get('Medium', 0) for model in severity_counts),
            'High': sum(severity_counts[model].get('High', 0) for model in severity_counts),
        }

        health_score = calculate_organization_health()

        context = {
            'domains_count': domains_count,
            'cards_count': cards_count,
            'pii_exposures_count': pii_exposures_count,
            'stealer_logs_count': stealer_logs_count,
            'severity_counts': severity_counts,
            'total_severity_counts': total_severity_counts,
            'health_score' : health_score
        }

        return render(request, "dashboard.html", context)

class DomainView(LoginRequiredMixin, View):
    login_url = "login"
    
    def get(self, request):
        domains = Domain.objects.all()
        domain_length = len(domains)
        all_domains = [domain.name for domain in domains]
        unique_domain = set(all_domains)
        unique_domain_length = len(unique_domain)
        
        leak_sources = {}
        for domain_obj in domains:
            name = domain_obj.name
            source_domain = domain_obj.source_domain
            if name not in leak_sources:
                leak_sources[name] = []
            # Count occurrences of each domain for a bin
            domain_exists = next((item for item in leak_sources[name] if item["domain"] == source_domain), None)
            if domain_exists:
                domain_exists["count"] += 1
            else:
                leak_sources[name].append({"count": 1, "domain": source_domain})
        
        leak_sources_json = json.dumps(leak_sources)

        return render(request, "domain.html", {'domains': domains, 'domain_length': domain_length, 'unique_domain_length': unique_domain_length, 'unique_domains': unique_domain, 'leak_sources_json': leak_sources_json})
    
class CardsView(LoginRequiredMixin, View):
    login_url = "login"
    
    def get(self, request):
        cards = Card.objects.all()
        card_length = len(cards)
        card_bin_numbers = [card.card_bin_number for card in cards]
        unique_card_bin_numbers = set(card_bin_numbers)
        unique_card_length = len(unique_card_bin_numbers)
        
        # Prepare the leakSources data
        leak_sources = {}
        for card in cards:
            bin_number = card.card_bin_number
            domain = card.breach_source_domain
            if bin_number not in leak_sources:
                leak_sources[bin_number] = []
            # Count occurrences of each domain for a bin
            domain_exists = next((item for item in leak_sources[bin_number] if item["domain"] == domain), None)
            if domain_exists:
                domain_exists["count"] += 1
            else:
                leak_sources[bin_number].append({"count": 1, "domain": domain})
        
        leak_sources_json = json.dumps(leak_sources)

        return render(request, "cards.html", {
            'cards': cards,
            'card_length': card_length,
            'unique_card_length': unique_card_length,
            'unique_card_bin_numbers': unique_card_bin_numbers,
            'leak_sources_json': leak_sources_json
        })

class EmailView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self,request):
        return render(request, "email.html")
    
class OrganizationDetailsView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "organization-details.html")
    
class NotificationsAlertView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "notification-alerts.html")

class BlackMarketView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        black_market_datas = BlackMarket.objects.all()
        return render(request, "black_market.html",{'black_market_datas': black_market_datas})
    
class StealerLogsView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        stealer_logs = StealerLogs.objects.all()
        return render(request, "stealer-logs.html",{'stealer_logs': stealer_logs})

class PiiExposureView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        # Retrieve all PII exposures from the database
        pii_exposures = PIIExposure.objects.all()

        # Calculate the total number of PII exposures
        pii_exposures_length = pii_exposures.count()

        # Extract unique email addresses from PII exposures
        pii_exposures_emails = [pii_exposure.personal_email for pii_exposure in pii_exposures]
        unique_pii_exposures_emails = set(pii_exposures_emails)
        unique_pii_exposures_length = len(unique_pii_exposures_emails)

        # Prepare leak sources data
        leak_sources = {}
        for pii_exposure in pii_exposures:
            email = pii_exposure.personal_email
            domain = pii_exposure.source_domain
            if email not in leak_sources:
                leak_sources[email] = []
            # Count occurrences of each domain for an email
            domain_exists = next((item for item in leak_sources[email] if item["domain"] == domain), None)
            if domain_exists:
                domain_exists["count"] += 1
            else:
                leak_sources[email].append({"count": 1, "domain": domain})
        
        # Convert leak_sources dictionary to JSON
        leak_sources_json = json.dumps(leak_sources)

        # Render the template with the necessary context data
        return render(request, "pii-exposure.html", {
            'pii_exposures': pii_exposures,
            'pii_exposures_length': pii_exposures_length,
            'unique_pii_exposures_length': unique_pii_exposures_length,
            'unique_pii_exposures_emails': unique_pii_exposures_emails,
            'leak_sources_json': leak_sources_json
        })


class Overview(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "overview.html")
        
class ThreatIntelligence(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        url = 'https://api.any.run/v1/feeds/stix.json?IP=true&Domain=true&URL=true'
        token = 'WX2JCzLFjmaRXaQHFhLfbfn5EHdwxCmbBpY8tQ78'

        headers = {
            'Accept': '*/*',
            'Authorization': f'API-Key {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            context = {'error': 'Error fetching the API', 'details': response.text}
        else:
            context =  response.json()

        types = defaultdict(int)
        for obj in context["data"]["objects"]:
            types[obj["type"]] += 1
         # Convert to a list and sort
        context["types"] = sorted(types.keys())
        print("types: ", context["types"])

        return render(request, "threatIntelligence.html",{'context':context})
class ThreatActor(LoginRequiredMixin, View):
    login_url = "login"
    
    def get(self, request):
        url = "https://api.feedly.com/v3/entities/nlp%2Ff%2Fentity%2Fgz%3Ata%3A68391641-859f-4a9a-9a1e-3e5cf71ec376"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer 68391641-859f-4a9a-9a1e-3e5cf71ec376"
        }
        response = requests.get(url, headers=headers)
     
        if response.status_code != 200:
            context = {'error': 'Error fetching the API', 'details': response.text}
        else:
            context = {'data': response.json()}
        print(context)

        return render(request, "threatActorProfile.html", {'context':context})
