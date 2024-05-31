from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
import re

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
            return render(request, "register.html", {"error": str(e.messages)})

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
    def get(self,request):
        return render(request, "login.html")
    
    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
    
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(View):
    def get(self, request):
        return render(request, "home.html")
    