from django.contrib import admin
from django.db import connection
from .models import Airline, Airport, Route, Customers, CustomerProfiles
from orders.models import Leg, Reservation
from accounts.models import Profile
from django.contrib.auth.models import User
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(admin.ModelAdmin):
  inlines = (ProfileInline, )
    # form = CustomerForm
  fields = (
          'username',
          'first_name',
          'last_name',
          'email',
          'is_active'
        )
  list_display = (
    'username',
    'first_name',
    'last_name',
    'email',
    'is_active'
  )

class RouteModelAdmin(admin.ModelAdmin):

  list_display = (
    'id',
    'airline_id',
    'flight_no',
    'src_airport',
    'dst_airport',
    'num_of_seats',
    'num_of_stops',
    'src_time',
    'dst_time',
    'arrive_day',
    'working_days',
    'fare',
    'flying_time',
  )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Route, RouteModelAdmin)
