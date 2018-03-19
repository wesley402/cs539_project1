from django.contrib import admin
from .models import Airline
# Register your models here.

class AirlineAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "iata", "icao"]



admin.site.register(Airline, AirlineAdmin)
