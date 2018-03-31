from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext, loader
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import Route
from accounts.models import Profile
from django.contrib.auth.models import User
from django.core.cache import cache
from datetime import datetime
from django.db import connection
from itertools import chain
from django import template

register = template.Library()

@register.filter
def add(value, arg):
    return value + arg
#def index(request):
#    all_airlines = Airline.objects.all()
    #html = ''
    #for p in Airline.objects.raw('SELECT * FROM polls_airline'):
    #for airline in all_airlines:
        #url = '/music/' + str(airline.id) + '/'
        #html += '<a href="' + url + '">' + airline.name + '</a><br>'
#        html += p.name
#retrn HttpResponse(html)


def home(request):
    return render(request, 'mysite/index.html', {
        'foo': 'bar',
    }, content_type='html')

def searchResults(request):

    trip = request.GET.get('trip')
    if(trip == 'oneway'):
        city1  = request.GET.get('from')
        city2  = request.GET.get('to')
        nums_of_psgs = request.GET.get('numofpsgs')
        cabin = request.GET.get('cabin')
        raw_dep_date = request.GET.get('dep_date')

        # change to date object
        curr_date = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
        dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')
        diff_days = (dep_date - curr_date).days

        weekday = dep_date.strftime('%w') # date to weekday
        request.session['nums_of_psgs'] = nums_of_psgs
        request.session['cabin'] = cabin
        request.session['trip'] = trip
        request.session['raw_dep_date'] = raw_dep_date

        cursor = connection.cursor()
        cursor.callproc('getDirectOnewayTrip', [city1, city2, weekday])
        raw_directOnewayTrip_tuples = cursor.fetchall()
        cursor.close()

        raw_directOnewayTrip_lists = list(map(list, raw_directOnewayTrip_tuples))
        directOnewayTrip_lists = fareCalculator_1(raw_directOnewayTrip_lists, diff_days, cabin)
        cache.set('directOnewayTrip_lists', directOnewayTrip_lists)
        print(directOnewayTrip_lists)
        #return render(request, 'mysite/flight-search.html', {"directOnewayTrip_lists": directOnewayTrip_lists})

        cursor = connection.cursor()
        cursor.callproc('getOnestopOnewayTrip', [city1, city2, weekday])
        raw_oneStopOnewayTrip_tuples = cursor.fetchall()
        cursor.close()
        raw_oneStopOnewayTrip_lists = list(map(list, raw_oneStopOnewayTrip_tuples))
        oneStopOnewayTrip_lists = fareCalculator_2(raw_oneStopOnewayTrip_lists, diff_days, cabin)
        print(oneStopOnewayTrip_lists)

        cache.set('oneStopOnewayTrip_lists', oneStopOnewayTrip_lists)
        return render(request, 'mysite/flight-search.html', {"oneStopOnewayTrip_lists": oneStopOnewayTrip_lists, "directOnewayTrip_lists": directOnewayTrip_lists})


    elif(search_type == 'roundtrip'):
        return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

    elif(search_type == 'multicity'):
        return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

    return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

def flightInfo(request):
    BOOKING_FEE_RATE = 0.02

    request.session['num_of_stops'] = request.GET.get('num_of_stops')
    if request.session['trip'] == 'oneway' and request.session['num_of_stops'] == '0':
        directOnewayTrip_lists = cache.get('directOnewayTrip_lists')
        print(directOnewayTrip_lists)
        table_index = int(request.GET.get('table_index'))
        cache.set('order_direct_flight',directOnewayTrip_lists[table_index])
        order_direct_flight = cache.get('order_direct_flight')
        booking_fee = order_direct_flight[7] * int(request.session['nums_of_psgs']) * BOOKING_FEE_RATE
        total_fare = order_direct_flight[7] * int(request.session['nums_of_psgs']) * (1 + BOOKING_FEE_RATE)
        request.session['booking_fee'] = booking_fee
        request.session['total_fare'] = total_fare
        return render(request, 'mysite/flight-information.html', {"table": order_direct_flight})

def bestSeller(request):
    cursor = connection.cursor()
    cursor.callproc('getBestSellers')
    bestSellers = cursor.fetchall()
    cursor.close()
    for i in bestSellers:
        print(i[0])
    return render(request, 'mysite/best-seller.html', {"bestSellers": bestSellers})

def fareCalculator_1(trip_lists, diff_days, cabin):
    ADVANCE_3_DAYS = 0.95
    ADVANCE_7_DAYS = 0.90
    ADVANCE_14_DAYS = 0.85
    ADVANCE_21_DAYS = 0.8
    E = 1.0 # Economy
    PE = 2.0 # Premium Economy
    B = 3.0 # Business
    FC = 4.0 # First Class

    for t in trip_lists:
        total_fare = t[7]

        if(diff_days >= 3 and diff_days < 7):
            total_fare = total_fare * ADVANCE_3_DAYS
        elif(diff_days >= 7 and diff_days < 14):
            total_fare = total_fare * ADVANCE_7_DAYS
        elif(diff_days >= 14 and diff_days < 21):
            total_fare = total_fare * ADVANCE_14_DAYS
        elif(diff_days >= 21):
            total_fare = total_fare * ADVANCE_21_DAYS

        if(cabin == 'economy'):
            total_fare = total_fare * E
        elif(cabin == 'premium economy'):
            total_fare = total_fare * PE
        elif(cabin == 'business'):
            total_fare = total_fare * B
        else: # First Class`
            total_fare = total_fare * FC

        t[7] = total_fare

    return trip_lists

def fareCalculator_2(trip_lists, diff_days, cabin):
    ADVANCE_3_DAYS = 0.95
    ADVANCE_7_DAYS = 0.90
    ADVANCE_14_DAYS = 0.85
    ADVANCE_21_DAYS = 0.8
    E = 1.0 # Economy
    PE = 2.0 # Premium Economy
    B = 3.0 # Business
    FC = 4.0 # First Class

    for t in trip_lists:
        total_fare = t[19]

        if(diff_days >= 3 and diff_days < 7):
            total_fare = total_fare * ADVANCE_3_DAYS
        elif(diff_days >= 7 and diff_days < 14):
            total_fare = total_fare * ADVANCE_7_DAYS
        elif(diff_days >= 14 and diff_days < 21):
            total_fare = total_fare * ADVANCE_14_DAYS
        elif(diff_days >= 21):
            total_fare = total_fare * ADVANCE_21_DAYS

        if(cabin == 'economy'):
            total_fare = total_fare * E
        elif(cabin == 'premium economy'):
            total_fare = total_fare * PE
        elif(cabin == 'business'):
            total_fare = total_fare * B
        else: # First Class`
            total_fare = total_fare * FC

        t[19] = total_fare

    return trip_lists

def isFlightFull(): # return the list of full flight
    return False




def action(request):
    if request.method == 'POST':
        action = request.POST['actionSelect']
        print(action)
        if 'customer' in action.lower():
            return redirect('manage_customers')
        elif 'reservation'in action.lower():
            return redirect('manage_reservations')
        elif 'flight' in action.lower():
            return redirect('flights')
        elif 'report' in action.lower():
            return redirect('reports')
        else:
            return redirect('admin')
    else:
        return redirect('admin')
        
# Create your views here.
def manage_customers(request):
    context={
        'title': 'Manage Customers'
    }
    return render(request,"admin/manage_customers.html",context=context)

def manage_reservations(request):
    context={
        'title': 'Manage Reservations'
    }
    return render(request,"admin/manage_reservations.html",context=context)

def view_flights(request):
    context={
        'title': 'View Flights'
    }
    return render(request,"admin/flights.html",context=context)

def generate_reports(request):
    context={
        'title': 'Reporting'
    }
    return render(request,"admin/reporting.html",context=context)