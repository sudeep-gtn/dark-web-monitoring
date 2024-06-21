from django.urls import path
from .views import (
    RegisterView, LoginView,
    HomeView, LogoutView,
    ProfileView,
    TermsAndConditionsView,
    BrandProtectionView, EditNameView,
    ChangePasswordView, ContactPageView,
    VerifyOTP, SendOTPFromProfile
    )

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login', LoginView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('terms-and-conditions', TermsAndConditionsView.as_view(), name='''terms-
         and-conditions'''),
    path('brand-protection', BrandProtectionView.as_view(), name="brand-protection"),
    path('edit-name', EditNameView.as_view(), name="edit-name"),
    path('change-password', ChangePasswordView.as_view(), name="change-password"),
    path('contact', ContactPageView.as_view(), name="contact"),
    path('verify-otp', VerifyOTP.as_view(), name="verify-otp"),
    path('send-otp-now', SendOTPFromProfile.as_view(), name="send-otp-now")
    ]
