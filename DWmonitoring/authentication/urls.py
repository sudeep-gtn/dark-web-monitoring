from django.urls import path
from .views import RegisterView, LoginView, HomeView, LogoutView, DashboardView

urlpatterns = [
    path('',HomeView.as_view(), name="home"),
    path('login',LoginView.as_view(), name="login"),
    path('register',RegisterView.as_view(), name="register"),
    path('logout',LogoutView.as_view(), name="logout"),
    path('dashboard',DashboardView.as_view(), name="dashboard"),
]
