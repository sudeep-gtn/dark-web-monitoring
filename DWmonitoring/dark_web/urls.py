from django.urls import path
from .views import (
    DomainView, 
    CardsView, 
    EmailView, OrganizationDetailsView, 
    NotificationsView, 
    BlackMarketView, StealerLogsView, 
    PiiExposureView,DashboardView
    )
urlpatterns = [
    path('dark-web-monitoring/dashboard',DashboardView.as_view(), name="dashboard"),
    path('dark-web-monitoring/leaks/domain',DomainView.as_view(), name="domain"),
    path('dark-web-monitoring/cards',CardsView.as_view(), name="cards"),
    path('details/email',EmailView.as_view(), name="email"),
    path('org-details', OrganizationDetailsView.as_view(), name="org-details"),
    path('notifications',NotificationsView.as_view(), name="notifications"),
    path('dark-web-monitoring/leaks/black-market',BlackMarketView.as_view(), name="black-market"),
    path('dark-web-monitoring/leaks/stealer-logs', StealerLogsView.as_view(), name="stealer-logs"),
    path('dark-web-monitoring/leaks/pii-exposure', PiiExposureView.as_view(),name="pii-exposure"),
]