from django.contrib import admin
from .models import CustomUser, UserLoginHistory

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserLoginHistory)
