from django.contrib import admin
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite


# Register your models here.
class MyAdminSite(AdminSite):
    site_header = 'Monty Python administration'

admin_site = MyAdminSite(name='myadmin')
admin_site.register([User,Profile])