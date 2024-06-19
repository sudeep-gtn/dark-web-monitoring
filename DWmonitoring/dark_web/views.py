from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Card, Domain, BlackMarket, Notification, StealerLogs, PIIExposure, calculate_organization_health
import json
import requests
from collections import defaultdict
from cybernews.cybernews import CyberNews
from dateutil import parser

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        # Counts for all instances
        domains_count = Domain.objects.count()
        cards_count = Card.objects.count()
        pii_exposures_count = PIIExposure.objects.count()
        stealer_logs_count = StealerLogs.objects.count()

        health_score = calculate_organization_health()

        context = {
            'domains_count': domains_count,
            'cards_count': cards_count,
            'pii_exposures_count': pii_exposures_count,
            'stealer_logs_count': stealer_logs_count,
            'health_score': health_score
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
        
        # Prepare the leakSources data reversed
        reversed_leak_sources = {}
        for card in cards:
            bin_number = card.card_bin_number
            domain = card.breach_source_domain
            if domain not in reversed_leak_sources:
                reversed_leak_sources[domain] = []
            # Count occurrences of each bin number for a domain
            bin_exists = next((item for item in reversed_leak_sources[domain] if item["bin_number"] == bin_number), None)
            if bin_exists:
                bin_exists["count"] += 1
            else:
                reversed_leak_sources[domain].append({"count": 1, "bin_number": bin_number})
        
        reversed_leak_sources_json = json.dumps(reversed_leak_sources)

        return render(request, "cards.html", {
            'cards': cards,
            'card_length': card_length,
            'unique_card_length': unique_card_length,
            'unique_card_bin_numbers': unique_card_bin_numbers,
            'reversed_leak_sources_json': reversed_leak_sources_json
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
        notifications = Notification.objects.all().order_by('-timestamp')
        notifications_length = len(notifications)
        return render(request, 'notificationsAlert.html', {'notifications': notifications, 'notifications_length': notifications_length})
 

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
        pii_exposures = PIIExposure.objects.all()

        pii_exposures_length = pii_exposures.count()

        pii_exposures_emails = [pii_exposure.personal_email for pii_exposure in pii_exposures]
        unique_pii_exposures_emails = set(pii_exposures_emails)
        unique_pii_exposures_length = len(unique_pii_exposures_emails)

        leak_sources = {}
        for pii_exposure in pii_exposures:
            email = pii_exposure.personal_email
            domain = pii_exposure.source_domain
            if email not in leak_sources:
                leak_sources[email] = []

            domain_exists = next((item for item in leak_sources[email] if item["domain"] == domain), None)
            if domain_exists:
                domain_exists["count"] += 1
            else:
                leak_sources[email].append({"count": 1, "domain": domain})
        
        leak_sources_json = json.dumps(leak_sources)

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
        health_score = calculate_organization_health()
        context = {
            'health_score': health_score
        }
        return render(request, "overview.html", context)
        
class ThreatIntelligence(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        news = CyberNews()
        
        malware_news = news.get_news('malware')
        
        news_data =malware_news
        for news_item in news_data:
            try:
                news_item['newsDate'] = parser.parse(news_item['newsDate']).date()
            except ValueError:
                print("The date is not in correct date format")
                news_item['newsDate'] = None
        news_data = [item for item in news_data if item['newsDate'] is not None]
        news_data_sorted = sorted(news_data, key=lambda x: x['newsDate'], reverse=True)
        total_news = len(news_data_sorted)

        print("malware news : ", news_data_sorted)
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
         
        context["types"] = sorted(types.keys())
        print("types: ", context["types"])

        return render(request, "threatIntelligence.html",{'context':context, 'news_data_sorted'  : news_data_sorted })
    
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

        return render(request, "threatActorProfile.html", {'context':context})



class IncidentResponse(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, 'incidentResponse.html')


    
class AnalyticsAndReports(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        breach_dates = ['2023-01-15', '2023-02-10', '2023-03-05', '2023-04-25', '2023-05-12', '2023-06-08']
        breach_counts = [1, 2, 1, 1, 1, 2]
        context = {
            'breach_dates': breach_dates,
            'breach_counts': breach_counts,
        }        
        return render( request,'analyticsAndReports.html', {'context':context})


class LiveThreatMap(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "liveThreatMap.html")
    

from django.shortcuts import render
from django.http import HttpResponse
from .models import Domain
from weasyprint import HTML
from django.template.loader import render_to_string

def generate_report(request):
    # Fetch data from the database
    domains = Domain.objects.all()

    print("domain: ", domains)
    # Render the HTML template with the data
    html_string = render_to_string('report_template.html', {'domains': domains})

    # Convert the rendered HTML to PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Create a response with the PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response