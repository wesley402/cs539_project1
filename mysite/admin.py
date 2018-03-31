from django.contrib import admin
from django.db import connection

from .models import Airline, Airport, Route
from orders.models import Leg, Reservation
from accounts.models import Profile
# Register your models here.



# class AirlineAdmin(admin.ModelAdmin):
#     # get list of columns
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM dbproject.mysite_airline;')
#         columns = [col[0] for col in cursor.description]

#     list_display = columns

# admin.site.register(Airline, AirlineAdmin)

# class AirportAdmin(admin.ModelAdmin):
#     # get list of columns
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM dbproject.mysite_airport;')
#         columns = [col[0] for col in cursor.description]

#     list_display = columns

# class RouteAdmin(admin.ModelAdmin):
#     # get list of columns
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM dbproject.mysite_route')
#         columns = [col[0] for col in cursor.description]

#     list_display = columns

# class ReservationAdmin(admin.ModelAdmin):
#     # get list of columns
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM dbproject.orders_reservation;')
#         columns = [col[0] for col in cursor.description]

#     list_display = columns
#     search_fields = ['username','reservation_date','fare_restrictions','reservation_status']
#     list_filter = ('reservation_date','fare_restrictions','reservation_status')

# class CustomerAdmin(admin.ModelAdmin):
#     # get list of columns
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM dbproject.accounts_profile;')
#         columns = [col[0] for col in cursor.description]

#     list_display = columns

# admin.site.register(Profile, CustomerAdmin)
# admin.site.register(Reservation, ReservationAdmin)
# admin.site.register(Route, RouteAdmin)

# admin.site.register(Airport, AirportAdmin)


admin.site.site_header = 'Site Administration'
admin.site.site_title = 'Site Administration'
