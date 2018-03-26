from django.shortcuts import render
from .models import Reservation
from django.http import HttpResponse
from django.core.cache import cache
import datetime
# Create your views here.
def checkout(request):
    if request.method == 'POST':
        flight=cache.get('order_flight')
        now = datetime.datetime.now()
        reserv_no = 'TX' + now.strftime('%Y%m%d%H%M%S%f')
        Reservation.objects.create(
            username=request.user.username,
            reservation_no=reserv_no, num_legs=flight.num_of_stops,
            fare_restrictions='ssss', passengers='ssssss',
            total_fare=12312312, booking_fee=13123123, customer_rep='cscsc')
        return HttpResponse("<h>Your Order is Accecpted !!!!!!</h>")

    else:
        nums_of_psgs = int(request.session['nums_of_psgs'])
        return render(request, 'orders/checkout.html', {'range':range(nums_of_psgs)})

def order(request):
    return render(request, 'orders/order.html')
