from django.shortcuts import render
from .models import Reservation, Leg
from django.http import HttpResponse
from django.core.cache import cache
from datetime import datetime
import random

# Create your views here.
def checkout(request):
    if request.method == 'POST':
        flight=cache.get('order_flight')
        now = datetime.now()
        reserv_no = 'TX' + now.strftime('%Y%m%d%H%M%S%f')
        ppls = ''
        order_direct_flight = cache.get('order_direct_flight')

        for i in range(int(request.session['nums_of_psgs'])):
            first_name = 'first_name' + str(i)
            last_name = 'last_name' + str(i)
            ppls = ppls + request.POST[first_name] + ' ' + request.POST[last_name] + ','


        raw_dep_date = request.session['raw_dep_date']
        dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')

        Reservation.objects.create(
            username=request.user.username,
            reservation_no=reserv_no,
            num_legs= int(request.session['num_of_stops']) + 1,
            fare_restrictions='',
            passengers = ppls,
            total_fare = float(request.session['total_fare']),
            booking_fee = float(request.session['booking_fee']),
            customer_rep ='wesley')

        Leg.objects.create(
            reservation_no=reserv_no,
            leg_no = 1,
            airline_id = order_direct_flight[0],
            flight_no = order_direct_flight[1],
            src_airport = order_direct_flight[2],
            dst_airport = order_direct_flight[3],
            src_time = dep_date.strftime('%Y-%m-%d') + ' ' + order_direct_flight[4].strftime('%H:%M'),
            dst_time = dep_date.strftime('%Y-%m-%d') + ' ' + order_direct_flight[5].strftime('%H:%M'),
            cabin = request.session['cabin'],
            seat_num = random.randint(0, 100),
        )

        return HttpResponse("<h>Your Order is Accecpted !!!!!!</h>")

    else:
        nums_of_psgs = int(request.session['nums_of_psgs'])
        return render(request, 'orders/checkout.html', {'range':range(nums_of_psgs)})

def order(request):
    return render(request, 'orders/order.html')

def history_order(request):
    orderLists = Reservation.objects.filter(username=request.user.username)
    if orderLists.exists():
        return render(request, 'orders/history_order.html', {'orderLists': orderLists})
    else:
        return HttpResponse("<h>No Order History Exists !!!!!!</h>")
def current_order(request):
    #currOrderLists = Reservation.objects.raw('SELECT * FROM orders_reservation WHERE reservation_status =%s AND username =%s',['S', request.user.username])
    currOrderLists = Reservation.objects.filter(reservation_status='A', username=request.user.username)
    if currOrderLists.exists():
        return render(request, 'orders/current_order.html', {'currOrderLists': currOrderLists})
    else:
        return HttpResponse("<h>No Current Order Exists !!!!!!</h>")
