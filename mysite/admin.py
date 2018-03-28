from django.contrib import admin
from .models import Airline, Airport, Route
from django.db import connection
from orders.models import Leg, Reservation
# Register your models here.

class AirlineAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class RouteAdmin(admin.ModelAdmin):
    # get list of columns
    with connection.cursor() as cursor:
        cursor.callproc('getAllFlights')
        columns = [col[0] for col in cursor.description]

    list_display = columns

class ReservationAdmin(admin.ModelAdmin):
    # get list of columns
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM dbproject.orders_reservation;')
        columns = [col[0] for col in cursor.description]

    list_display = columns

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Airline, AirlineAdmin)