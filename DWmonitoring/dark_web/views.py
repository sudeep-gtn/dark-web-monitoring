from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Card

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "dashboard.html")
    
    
class DomainView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "domain.html")
    
class CardsView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        cards = Card.objects.all()
        card_length = len(cards)
        card_bin_numbers = [card.card_bin_number for card in cards]
        unique_card_bin_numbers = set(card_bin_numbers)
        unique_card_length = len(unique_card_bin_numbers)
        
        return render(request, "cards.html", {'cards': cards, 'card_length': card_length, 'unique_card_length': unique_card_length, 'unique_card_bin_numbers':unique_card_bin_numbers})
    
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
        return render(request, "black_market.html")
    
class StealerLogsView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "stealer-logs.html")
    

class PiiExposureView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "pii-exposure.html")
    