from django.contrib import admin
from django.db import connection
from .models import Airline, Airport, Route, Customers, CustomerProfiles
from orders.models import Leg, Reservation
from accounts.models import Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Reservation)