from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid Password"})

class LogoutView(View, LoginRequiredMixin):
    login_url = "login"
    def get(self, request):
        logout(request)
        return redirect("login")

class HomeView(View):
    def get(self, request):
        return render(request, "home.html")

class VerifyOTP(View):
    def get(self, request):
        return render(request, 'verify-otp.html')

class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "profile.html")

class TermsAndConditionsView(View):
    def get(self, request):
        return render(request, "terms_and_conditions.html")
    
class BrandProtectionView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "brand-protection.html")
    
class EditNameView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "profile.html")
    
    def post(self, request):
        user = request.user
        full_name = request.POST.get("full_name").strip()

        if not re.match(r'^[A-Za-z\s]{3,}$', full_name):
            messages.error(request, "Full name must be at least 3 characters long and contain only alphabetic characters and spaces")
            return redirect("profile")

        if full_name:
            user.full_name = full_name
            user.save()
            messages.success(request,"Name changed successfully")
            return redirect("profile")
        else:
            messages.error(request,"Something went wrong. Please try again.")
            return redirect("profile")

class ChangePasswordView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, "profile.html")
    
    def post(self, request):
        user = request.user
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        c_new_password = request.POST.get("c_new_password")

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("profile")
        
        if new_password != c_new_password:
            messages.error(request, "New passwords do not match.")
            return render(request, "profile.html")
        
        try:
            validate_password(new_password)
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return redirect("profile")
    
        user.set_password(new_password)
        user.save()
        
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully.")
        return redirect("profile")

class ContactPageView(View):
    def get(self, request):
        return render(request, "contact.html")