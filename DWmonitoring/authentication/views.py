from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        full_name = request.POST.get("full_name").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        c_password = request.POST.get("c_password").strip()

        if not re.match(r'^[A-Za-z\s]{3,}$', full_name):
            return render(request, "register.html", {"error": "Full name must be at least 3 characters long and contain only alphabetic characters and spaces"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "User with the provided email already exists"})

        if password != c_password:
            return render(request, "register.html", {"error": "Passwords do not match"})
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "register.html", {"error": "Invalid email address"})

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, "register.html", {"error": "".join(e.messages)})

        try:
            user = CustomUser.objects.create_user(
                email=email, full_name=full_name, password=password
            )

        except Exception as e:
            return render(request, "register.html", {"error": "Registration failed"})

        if user:
            return redirect("login")
        else:
            return render(request, "register.html", {"error": "Registration failed"})

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, "login.html", {"error": "User with the provided email does not exist"})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "login.html", {"error": "Invalid Password"})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(View):
    def get(self, request):
        return render(request, "home.html")

class DashboardView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "dashboard.html")
    
class DomainView(View):
    def get(self, request):
        return render(request,"domain.html")
    
class CardsView(View):
    def get(self, request):
        return render(request,"cards.html")
    
class UsersView(View):
    def get(self, request):
        return render(request,"users.html")
    
class EmailView(View):
    def get(self,request):
        return render(request, "email.html")
    
class OrganizationDetailsView(View):
    def get(self, request):
        return render(request,"organization-details.html")
    
class NotificationsView(View):
    def get(self, request):
        return render(request,'notifications.html')