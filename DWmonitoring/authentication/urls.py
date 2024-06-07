from django.urls import path
from .views import (
    RegisterView, LoginView, 
    HomeView, LogoutView, 
    DashboardView, DomainView, 
    CardsView, UsersView, 
    EmailView, OrganizationDetailsView, 
    NotificationsView, ProfileView, 
    BlackMarketView, StealerLogsView, 
    PiiExposureView, TermsAndConditionsView,
    BrandProtectionView,EditNameView,
    ChangePasswordView
    )

urlpatterns = [
    path('',HomeView.as_view(), name="home"),
    path('login',LoginView.as_view(), name="login"),
    path('register',RegisterView.as_view(), name="register"),
    path('logout',LogoutView.as_view(), name="logout"),
    path('dark-web-monitoring/dashboard',DashboardView.as_view(), name="dashboard"),
    path('dark-web-monitoring/leaks/domain',DomainView.as_view(), name="domain"),
    path('dark-web-monitoring/cards',CardsView.as_view(), name="cards"),
    path('details/user',UsersView.as_view(), name="users"),
    path('details/email',EmailView.as_view(), name="email"),
    path('org-details', OrganizationDetailsView.as_view(), name="org-details"),
    path('notifications',NotificationsView.as_view(), name="notifications"),
    path('profile',ProfileView.as_view(), name="profile"),
    path('dark-web-monitoring/leaks/black-market',BlackMarketView.as_view(), name="black-market"),
    path('dark-web-monitoring/leaks/stealer-logs', StealerLogsView.as_view(), name="stealer-logs"),
    path('dark-web-monitoring/leaks/pii-exposure', PiiExposureView.as_view(),name="pii-exposure"),
    path('terms-and-conditions', TermsAndConditionsView.as_view(), name="terms-and-conditions"),
    path('brand-protection',BrandProtectionView.as_view(), name="brand-protection"),
    path('edit-name', EditNameView.as_view(), name="edit-name"),
    path('change-password', ChangePasswordView.as_view(), name="change-password")
]
