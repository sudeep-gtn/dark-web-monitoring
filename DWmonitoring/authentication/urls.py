from django.urls import path
from .views import RegisterView, LoginView, HomeView, LogoutView, DashboardView, DomainView, CardsView, UsersView, EmailView, OrganizationDetailsView, NotificationsView, ProfileView, BlackMarketView, StellarLogsView, PiiExposureView

urlpatterns = [
    path('',HomeView.as_view(), name="home"),
    path('login',LoginView.as_view(), name="login"),
    path('register',RegisterView.as_view(), name="register"),
    path('logout',LogoutView.as_view(), name="logout"),
    path('dashboard',DashboardView.as_view(), name="dashboard"),
    path('leaks/domain',DomainView.as_view(), name="domain"),
    path('details/cards',CardsView.as_view(), name="cards"),
    path('details/user',UsersView.as_view(), name="users"),
    path('details/email',EmailView.as_view(), name="email"),
    path('org-details', OrganizationDetailsView.as_view(), name="org-details"),
    path('notifications',NotificationsView.as_view(), name="notifications"),
    path('profile',ProfileView.as_view(), name="profile"),
    path('leaks/black-market',BlackMarketView.as_view(), name="black-market"),
    path('leaks/stellar-logs', StellarLogsView.as_view(), name="stellar-logs"),
    path('leaks/pii-exposure', PiiExposureView.as_view(),name="pii-exposure")
]
