from django.contrib import admin
from .models import Airline, Route
# Register your models here.

class AirlineAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "iata", "icao"]

class RouteAdmin(admin.ModelAdmin):
    list_display = ["flight_no"]

admin.site.register(Route, RouteAdmin)
admin.site.register(Airline, AirlineAdmin)
