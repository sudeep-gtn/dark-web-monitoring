from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Card, Domain, BlackMarket, StealerLogs
import json

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "dashboard.html")
    
    
class DomainView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        domains = Domain.objects.all()
        domain_length = len(domains)
        all_domains = [domain.name for domain in domains]
        unique_domain = set(all_domains)
        unique_domain_length = len(unique_domain)
        return render(request, "domain.html",{'domains': domains, 'domain_length': domain_length, 'unique_domain_length': unique_domain_length})
    
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
    
class NotificationsView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "notifications.html")

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
        return render(request, "pii-exposure.html")
    