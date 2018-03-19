from django.db import models

# Create your models here.
class Airline(models.Model):
    name = models.CharField(max_length=60)
    iata = models.CharField(max_length=2, null=True)
    icao = models.CharField(max_length=3, null=True)




class Route(models.Model):
    flight_no = models.CharField(max_length=10, null=False)
    src_airport = models.CharField(max_length=4, null=False)
    dst_airport = models.CharField(max_length=4, null=False)
    num_of_stops = models.IntegerField(null=True)
    src_time = models.TimeField(null=False)
    dst_time = models.TimeField(null=False)
    #Fares = models.IntegerField(null=True)
    #Working_days = models.CharField(null=False)
