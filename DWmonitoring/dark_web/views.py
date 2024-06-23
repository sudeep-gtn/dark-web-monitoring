from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Card, Domain, BlackMarket, Notification, StealerLogs, PIIExposure, Ticket, calculate_organization_health
import json
import requests
from collections import defaultdict
from cybernews.cybernews import CyberNews
from dateutil import parser
from django.http import HttpResponse, HttpResponseBadRequest
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import JsonResponse

class DashboardView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
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

        # Domain.objects.create(
        #     name='example.com',
        #     domain_ip='192.168.1.1',
        #     source_ip='10.0.0.1',
        #     source_domain='example-source.com',
        #     breach_date='2024-03-10'
        # )

        # Domain.objects.create(
        #     name='testsite.org',
        #     domain_ip='172.16.0.1',
        #     source_ip='192.168.0.1',
        #     source_domain='testsite-source.org',
        #     breach_date='2023-11-05'
        # )

        # Domain.objects.create(
        #     name='mywebsite.net',
        #     domain_ip='203.0.113.1',
        #     source_ip='198.51.100.1',
        #     source_domain='mywebsite-source.net',
        #     breach_date='2024-02-20'
        # )

        # Domain.objects.create(
        #     name='anothersite.io',
        #     domain_ip='198.51.100.2',
        #     source_ip='203.0.113.2',
        #     source_domain='anothersite-source.io',
        #     breach_date='2024-01-15'
        # )

        # Domain.objects.create(
        #     name='sampledomain.edu',
        #     domain_ip='203.0.113.3',
        #     source_ip='198.51.100.3',
        #     source_domain='sampledomain-source.edu',
        #     breach_date='2024-05-18'
        # )

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

        # Card.objects.create(
        #     card_bin_number=123456,
        #     card_type='Visa',
        #     expiry_date='2025-12-31',
        #     cvv=123,
        #     card_holder_name='John Doe',
        #     issuing_bank='Bank of America',
        #     breach_date='2024-01-15',
        #     breach_source='Data Breach XYZ',
        #     last_used_date='2024-05-20',
        #     breach_source_domain='xyzbreach.com'
        # )

        # Card.objects.create(
        #     card_bin_number=654321,
        #     card_type='MasterCard',
        #     expiry_date='2023-07-31',
        #     cvv=321,
        #     card_holder_name='Jane Smith',
        #     issuing_bank='Chase Bank',
        #     breach_date='2023-02-10',
        #     breach_source='Data Breach ABC',
        #     last_used_date='2023-06-15',
        #     breach_source_domain='abcbreach.net'
        # )

        # Card.objects.create(
        #     card_bin_number=111111,
        #     card_type='American Express',
        #     expiry_date='2024-09-30',
        #     cvv=456,
        #     card_holder_name='Alice Johnson',
        #     issuing_bank='Wells Fargo',
        #     breach_date='2024-04-22',
        #     breach_source='Data Breach 123',
        #     last_used_date='2024-05-01',
        #     breach_source_domain='123breach.com'
        # )

        # Card.objects.create(
        #     card_bin_number=222222,
        #     card_type='Discover',
        #     expiry_date='2026-03-31',
        #     cvv=789,
        #     card_holder_name='Bob Brown',
        #     issuing_bank='Citi Bank',
        #     breach_date='2024-06-15',
        #     breach_source='Data Breach 456',
        #     last_used_date='2024-06-20',
        #     breach_source_domain='456breach.com'
        # )

        # Card.objects.create(
        #     card_bin_number=333333,
        #     card_type='Visa',
        #     expiry_date='2023-11-30',
        #     cvv=101,
        #     card_holder_name='Carol White',
        #     issuing_bank='HSBC',
        #     breach_date='2023-12-01',
        #     breach_source='Data Breach 789',
        #     last_used_date='2023-12-10',
        #     breach_source_domain='789breach.com'
        # )

        cards = Card.objects.all()
        card_length = len(cards)
        card_bin_numbers = [card.card_bin_number for card in cards]
        unique_card_bin_numbers = set(card_bin_numbers)
        unique_card_length = len(unique_card_bin_numbers)
        
        reversed_leak_sources = {}
        for card in cards:
            bin_number = card.card_bin_number
            domain = card.breach_source_domain
            if domain not in reversed_leak_sources:
                reversed_leak_sources[domain] = []
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

        # BlackMarket.objects.create(
        #     source='DarkWeb Market A',
        #     stealer_log_preview='Preview of stolen data...',
        #     related_assets='Credit cards, PII',
        #     price=199.99,
        #     status='Available',
        #     obtain_progress='10% completed',
        #     discovery_date='2024-04-22',
        #     incident='Incident 1234'
        # )

        # BlackMarket.objects.create(
        #     source='DarkWeb Market B',
        #     stealer_log_preview='Preview of different stolen data...',
        #     related_assets='Bank account details, SSNs',
        #     price=299.99,
        #     status='Sold',
        #     obtain_progress='100% completed',
        #     discovery_date='2023-10-10',
        #     incident='Incident 5678'
        # )

        # BlackMarket.objects.create(
        #     source='Black Market C',
        #     stealer_log_preview='Preview of more stolen data...',
        #     related_assets='Passwords, Usernames',
        #     price=399.99,
        #     status='Unavailable',
        #     obtain_progress='50% completed',
        #     discovery_date='2024-03-15',
        #     incident='Incident 9101'
        # )

        # BlackMarket.objects.create(
        #     source='DarkWeb Market D',
        #     stealer_log_preview='Another preview of stolen data...',
        #     related_assets='Credit reports, Addresses',
        #     price=149.99,
        #     status='Available',
        #     obtain_progress='70% completed',
        #     discovery_date='2024-02-28',
        #     incident='Incident 1121'
        # )

        # BlackMarket.objects.create(
        #     source='DarkWeb Market E',
        #     stealer_log_preview='Preview of various stolen data...',
        #     related_assets='Emails, Phone numbers',
        #     price=99.99,
        #     status='Sold',
        #     obtain_progress='90% completed',
        #     discovery_date='2024-01-10',
        #     incident='Incident 3141'
        # )

        black_market_datas = BlackMarket.objects.all()
        return render(request, "black_market.html",{'black_market_datas': black_market_datas})
    
class StealerLogsView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        # StealerLogs.objects.create(
        #     date_detected='2024-01-05',
        #     data_type='Credit Card Information',
        #     source='Malware XYZ',
        #     details='Details of the stolen data...'
        # )

        # StealerLogs.objects.create(
        #     date_detected='2023-08-12',
        #     data_type='Personal Identifiable Information',
        #     source='Spyware ABC',
        #     details='Details of the stolen PII...'
        # )

        # StealerLogs.objects.create(
        #     date_detected='2024-02-18',
        #     data_type='Bank Account Information',
        #     source='Malware DEF',
        #     details='Details of the stolen bank account information...'
        # )

        # StealerLogs.objects.create(
        #     date_detected='2023-09-25',
        #     data_type='Social Security Numbers',
        #     source='Spyware GHI',
        #     details='Details of the stolen SSNs...'
        # )

        # StealerLogs.objects.create(
        #     date_detected='2024-03-10',
        #     data_type='Email Addresses',
        #     source='Malware JKL',
        #     details='Details of the stolen email addresses...'
        # )

        stealer_logs = StealerLogs.objects.all()
        return render(request, "stealer-logs.html",{'stealer_logs': stealer_logs})

class PiiExposureView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):

        # PIIExposure.objects.create(
        #     name='John Doe',
        #     breach_date='2024-02-28',
        #     breach_ip='203.0.113.1',
        #     source_domain='breach-source.com',
        #     threat_type='Data Leak',
        #     type_of_data='Email, Phone Number',
        #     source='Breach Report XYZ',
        #     personal_email='john.doe@example.com',
        #     phone='+1234567890'
        # )

        # PIIExposure.objects.create(
        #     name='Jane Smith',
        #     breach_date='2023-09-15',
        #     breach_ip='198.51.100.2',
        #     source_domain='another-breach-source.net',
        #     threat_type='Unauthorized Access',
        #     type_of_data='SSN, Address',
        #     source='Breach Report ABC',
        #     personal_email='jane.smith@example.com',
        #     phone='+0987654321'
        # )

        # PIIExposure.objects.create(
        #     name='Alice Johnson',
        #     breach_date='2024-01-05',
        #     breach_ip='192.0.2.1',
        #     source_domain='third-breach-source.com',
        #     threat_type='Credential Theft',
        #     type_of_data='Username, Password',
        #     source='Breach Report 123',
        #     personal_email='alice.johnson@example.com',
        #     phone='+1123456789'
        # )

        # PIIExposure.objects.create(
        #     name='Bob Brown',
        #     breach_date='2023-08-25',
        #     breach_ip='198.51.100.3',
        #     source_domain='fourth-breach-source.net',
        #     threat_type='Phishing Attack',
        #     type_of_data='Bank Account, Routing Number',
        #     source='Breach Report 456',
        #     personal_email='bob.brown@example.com',
        #     phone='+2212345678'
        # )

        # PIIExposure.objects.create(
        #     name='Carol White',
        #     breach_date='2023-12-30',
        #     breach_ip='203.0.113.2',
        #     source_domain='fifth-breach-source.org',
        #     threat_type='Ransomware',
        #     type_of_data='PII, Financial Data',
        #     source='Breach Report 789',
        #     personal_email='carol.white@example.com',
        #     phone='+3321234567'
        # )


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
        




'''
<------------- threat intelligenece ---------->
'''
class ThreatIntelligence(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        news = CyberNews()
        malware_news = news.get_news('malware')
        
        news_data = malware_news
        for news_item in news_data:
            try:
                news_item['newsDate'] = parser.parse(news_item['newsDate']).date()
            except ValueError:
                print("The date is not in correct date format")
                news_item['newsDate'] = None
        
        news_data = [item for item in news_data if item['newsDate'] is not None]
        news_data_sorted = sorted(news_data, key=lambda x: x['newsDate'], reverse=True)
        
        return render(request, "threatIntelligence.html", {'news_data_sorted': news_data_sorted}) 
    


class FetchThreatIntelligenceData(LoginRequiredMixin, View):
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
            return JsonResponse({'error': 'Error fetching the API', 'details': response.text}, status=response.status_code)

        context = response.json()

        types = defaultdict(int)
        for obj in context["data"]["objects"]:
            types[obj["type"]] += 1
        
        context["types"] = sorted(types.keys())
        return JsonResponse(context)
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
        tickets = Ticket.objects.all()
        return render(request, 'incidentResponse.html', {'tickets': tickets})

    def post(self, request):
        ticket_title = request.POST.get('ticket_title')
        ticket_description = request.POST.get('ticket_description')
        image_file = request.FILES.get('image')
        
        new_ticket = Ticket(
            ticket_title=ticket_title,
            ticket_description=ticket_description,
            image=image_file
            )
        new_ticket.save()

        return redirect('incident-response')
    
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
    

from datetime import datetime

class GenerateReportView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'report_template.html')

    def post(self, request, *args, **kwargs):
        filters = request.POST.getlist('filters')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
        date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None

        print('filters: ', filters)
        print("date from ", date_from, "date to ", date_to)
        
        domains = []
        cards = []
        pii = []
        stealer_logs = []
        black_market = []

        # Fetch data from the database
        if 'domain-leaks' in filters:
            domains = Domain.objects.all()
            if date_from and date_to:
                domains = domains.filter(breach_date__range=(date_from, date_to))
        if 'card-leaks' in filters:
            cards = Card.objects.all()
            if date_from and date_to:
                cards = cards.filter(breach_date__range=(date_from, date_to))
        if 'pii-leaks' in filters:
            pii = PIIExposure.objects.all()
            if date_from and date_to:
                pii = pii.filter(breach_date__range=(date_from, date_to))
            
        if 'stealer_logs' in filters:
            stealer_logs = StealerLogs.objects.all()
            if date_from and date_to:
                stealer_logs = stealer_logs.filter(date_detected__range=(date_from, date_to))
            
        if 'black_market' in filters:
            black_market = BlackMarket.objects.all()
            if date_from and date_to:
                black_market = black_market.filter(discovery_date__range=(date_from, date_to))
            

        print("domain with filter: ", domains)
        print("cards with filter: ", cards)
        print("pii with filter: ", pii)

        context = {
            'domains': domains,
            'cards': cards,
            'pii': pii,
            'stealer_log':stealer_logs,
            'black_market': black_market
        }

        # Render the HTML template with the data
        html_string = render_to_string('report_template.html', context)

        # Convert the rendered HTML to PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Create a response with the PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
    

class PreviewReportView(View):
    def get(self, request, *args, **kwargs):
        filters = request.GET.getlist('filters')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
        date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None

        print('filters: ', filters)
        print("date from ", date_from, "date to ", date_to)
        
        domains = []
        cards = []
        pii = []
        black_market = []
        stealer_log = []
        # Fetch data from the database
        if 'domain-leaks' in filters:
            domains = Domain.objects.all()
            if date_from and date_to:
                domains = domains.filter(breach_date__range=(date_from, date_to))
        if 'card-leaks' in filters:
            cards = Card.objects.all()
            if date_from and date_to:
                cards = cards.filter(breach_date__range=(date_from, date_to))
        if 'pii-leaks' in filters:
            pii = PIIExposure.objects.all()
            if date_from and date_to:
                pii = pii.filter(breach_date__range=(date_from, date_to))


        if 'stealer_log' in filters:
            stealer_log = StealerLogs.objects.all()
            # if date_from and date_to:
            #     stealer_log = stealer_log.filter(date_detected__range=(date_from, date_to))
            
        if 'black_market' in filters:
            black_market = BlackMarket.objects.all()
            # if date_from and date_to:
            #     black_market = black_market.filter(discovery_date__range=(date_from, date_to))
            

        print("domain with filter: ", domains)
        print("cards with filter: ", cards)
        print("pii with filter: ", pii)
        print("balck ", black_market )
        print("Stealer:", stealer_log)
        context = {
            'domains': domains,
            'cards': cards,
            'pii': pii,
            'black_market':black_market,
            'stealer_log':stealer_log
        }

        # Render the template for preview
        return render(request, 'report_template.html', context)
    
    
class TicketsView(View):
    # def get(self, request):
    #     tickets = Ticket.objects.all()
    #     Ticket.objects.create(
    #         ticket_title='Data Breach on example.com',
    #         ticket_description='Details about the data breach on example.com...',
    #         resolved=False
    #     )

    #     Ticket.objects.create(
    #         ticket_title='Unauthorized Access on testsite.org',
    #         ticket_description='Details about the unauthorized access on testsite.org...',
    #         resolved=True
    #     )

    #     Ticket.objects.create(
    #         ticket_title='Vulnerability found on mywebsite.net',
    #         ticket_description='Details about the vulnerability found on mywebsite.net...',
    #         resolved=False
    #     )

    #     Ticket.objects.create(
    #         ticket_title='Suspicious login on anothersite.io',
    #         ticket_description='Details about the suspicious login on anothersite.io...',
    #         resolved=True
    #     )

    #     Ticket.objects.create(
    #         ticket_title='Data leak report for sampledomain.edu',
    #         ticket_description='Details about the data leak report for sampledomain.edu...',
    #         resolved=False
    #     )

    #     return render(request, "tickets.html", {'tickets': tickets})
    
    def post(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
        except Ticket.DoesNotExist:
            return HttpResponseBadRequest("Invalid Ticket ID")
        
        ticket.resolved = True
        ticket.save()
        return redirect('incident-response')




class SupportAndAssistance(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        return render(request,'support-and-assistance.html')
    
class TermsAndConditions(View):
    def get(self, request):
        return render(request, 'terms_and_conditions.html')