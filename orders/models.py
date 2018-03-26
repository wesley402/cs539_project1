from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    RESERVATION_STATUS = (
        ('A','Accepted'),
        ('C','Cancelled'),
    )
    reservation_no = models.CharField(max_length=100, blank=True, primary_key=True)
    reservation_date = models.DateTimeField(auto_now_add=True, blank=False)
    reservation_status = models.CharField(max_length=20, default = 'A', blank=False, choices=RESERVATION_STATUS)
    username = models.CharField(max_length=100, blank=True)
    num_legs = models.IntegerField(null=True)
    fare_restrictions = models.CharField(max_length=100, blank=True)
    passengers = models.CharField(max_length=100, blank=True)
    total_fare = models.FloatField(blank=True)
    booking_fee = models.FloatField(blank=True)
    customer_rep = models.CharField(max_length=25, blank=True)
    #customer_rep = models.ForeignKey(User,  to_field='username', on_delete=models.CASCADE)
    #username = models.ForeignKey(User,  to_field='username', on_delete=models.CASCADE)
