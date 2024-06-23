from django.urls import path
from .views import (
    DomainView, 
    CardsView, 
    EmailView, OrganizationDetailsView, 
    NotificationsAlertView, 
    BlackMarketView, StealerLogsView, 
    PiiExposureView,DashboardView,
    Overview,ThreatIntelligence, ThreatActor,
    IncidentResponse,AnalyticsAndReports,
    LiveThreatMap,GenerateReportView,PreviewReportView,
    TicketsView, FetchThreatIntelligenceData, SupportAndAssistance,
    TermsAndConditions
    )
urlpatterns = [
    path('dark-web-monitoring/dashboard', DashboardView.as_view(), name="dashboard"),
    path('dark-web-monitoring/compromised-data/domain', DomainView.as_view(), name="domain"),
    path('dark-web-monitoring/cards', CardsView.as_view(), name="cards"),
    path('details/email', EmailView.as_view(), name="email"),
    path('org-details', OrganizationDetailsView.as_view(), name="org-details"),
    path('notification-alerts', NotificationsAlertView.as_view(), name="notifications"),
    path('dark-web-monitoring/compromised-data/black-market', BlackMarketView.as_view(), name="black-market"),
    path('dark-web-monitoring/compromised-data/stealer-logs', StealerLogsView.as_view(), name="stealer-logs"),
    path('dark-web-monitoring/compromised-data/pii-exposure', PiiExposureView.as_view(),name="pii-exposure"),

    path('overview', Overview.as_view(), name='overview'),
    path('threat-intelligence', ThreatIntelligence.as_view(), name='threat-intelligence'),
    path('fetch-threat-intelligence-data/', FetchThreatIntelligenceData.as_view(), name='fetch_threat_intelligence_data'),


    path('threat-intelligence/actor/', ThreatActor.as_view(), name='threat-actor-profile'),
    path('incident-response', IncidentResponse.as_view(), name="incident-response"),
    path('analytics-and-reports', AnalyticsAndReports.as_view(), name="analytics-and-reports"),
    path('live-threatmap', LiveThreatMap.as_view(), name="live-threatmap"),
    path('report/', GenerateReportView.as_view() , name="generate_report"),
    path('preview-report/', PreviewReportView.as_view(), name="preview-report"),
    path('resolve/<int:ticket_id>/', TicketsView.as_view(), name='resolve_ticket'),

    path('support-and-assistance', SupportAndAssistance.as_view(), name='support-and-assistance'),
    path('terms-and-conditions', TermsAndConditions.as_view(), name='terms-and-conditions')

]