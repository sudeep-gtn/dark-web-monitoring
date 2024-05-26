from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")

        if password != c_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

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

# class Login(View):
#     def get(self,request):
#         return render(request, "login.html")
    
#     def post(self, request):
#         email = request.POST.get("email")
#         password = request.POST.get("password")

