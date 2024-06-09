from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

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
        return render(request, "cards.html")
    
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
    