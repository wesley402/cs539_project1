from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext, loader
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import Route
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
        num_of_psgs = request.GET.get('numofpsgs')
        cabin = request.GET.get('cabin')
        raw_dep_date = request.GET.get('dep_date')

        request.session['num_of_psgs'] = num_of_psgs
        request.session['cabin'] = cabin
        request.session['trip'] = trip
        request.session['raw_dep_date'] = raw_dep_date

        dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')
        weekday = dep_date.strftime('%w') # date to weekday

        cursor = connection.cursor()
        cursor.callproc('getDirectOnewayTrip', [city1, city2, weekday])
        raw_directOnewayTrip_tuples = cursor.fetchall()
        cursor.close()

        # change to date object
        curr_date = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
        diff_days = (dep_date - curr_date).days

        raw_directOnewayTrip_lists = list(map(list, raw_directOnewayTrip_tuples))
        directOnewayTrip_lists = fareCalculator_a(raw_directOnewayTrip_lists, diff_days, cabin)
        cache.set('directOnewayTrip_lists', directOnewayTrip_lists)
        #return render(request, 'mysite/flight-search.html', {"directOnewayTrip_lists": directOnewayTrip_lists})

        cursor = connection.cursor()
        cursor.callproc('getOnestopOnewayTrip', [city1, city2, weekday])
        raw_oneStopOnewayTrip_tuples = cursor.fetchall()
        cursor.close()

        raw_oneStopOnewayTrip_lists = list(map(list, raw_oneStopOnewayTrip_tuples))
        oneStopOnewayTrip_lists = fareCalculator_b(raw_oneStopOnewayTrip_lists, diff_days, cabin)
        cache.set('oneStopOnewayTrip_lists', oneStopOnewayTrip_lists)

        return render(request, 'mysite/flight-search-dst.html', {"oneStopOnewayTrip_lists": oneStopOnewayTrip_lists, "directOnewayTrip_lists": directOnewayTrip_lists})


    elif(trip == 'roundtrip'): # search first ticket
        city1  = request.GET.get('from')
        city2  = request.GET.get('to')
        num_of_psgs = request.GET.get('numofpsgs')
        cabin = request.GET.get('cabin')
        raw_dep_date = request.GET.get('dep_date')
        raw_rtn_date = request.GET.get('rtn_date')

        request.session['city1'] = city1
        request.session['city2'] = city2

        request.session['num_of_psgs'] = num_of_psgs
        request.session['cabin'] = cabin
        request.session['trip'] = trip
        request.session['raw_dep_date'] = raw_dep_date
        request.session['raw_rtn_date'] = raw_rtn_date


        dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')
        weekday = dep_date.strftime('%w') # date to weekday
        curr_date = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
        diff_days = (dep_date - curr_date).days

        dst_directOnewayTrip_lists = queryOnewayTrip(city1, city2, weekday, diff_days, request.session['cabin'], 'getDirectOnewayTrip')
        cache.set('dst_directOnewayTrip_lists', dst_directOnewayTrip_lists)

        dst_oneStopOnewayTrip_lists = queryOnewayTrip(city1, city2, weekday, diff_days, request.session['cabin'], 'getOnestopOnewayTrip')
        cache.set('dst_oneStopOnewayTrip_lists', dst_oneStopOnewayTrip_lists)

        return render(request, 'mysite/flight-search-dst.html', {"oneStopOnewayTrip_lists": dst_oneStopOnewayTrip_lists, "directOnewayTrip_lists": dst_directOnewayTrip_lists})



    return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})


def searchResults_rtn(request): # search second ticket

    request.session['dst_table_index'] = request.GET.get('table_index')
    request.session['dst_num_of_stops'] = request.GET.get('num_of_stops')

    city1 = request.session['city2']
    city2 = request.session['city1']

    raw_dep_date = request.session['raw_rtn_date']

    dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')
    weekday = dep_date.strftime('%w') # date to weekday
    curr_date = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
    diff_days = (dep_date - curr_date).days

    rtn_directOnewayTrip_lists = queryOnewayTrip(city1, city2, weekday, diff_days, request.session['cabin'], 'getDirectOnewayTrip')
    cache.set('rtn_directOnewayTrip_lists', rtn_directOnewayTrip_lists)

    rtn_oneStopOnewayTrip_lists = queryOnewayTrip(city1, city2, weekday, diff_days, request.session['cabin'], 'getOnestopOnewayTrip')
    cache.set('rtn_oneStopOnewayTrip_lists', rtn_oneStopOnewayTrip_lists)

    return render(request, 'mysite/flight-search-rtn.html', {"oneStopOnewayTrip_lists": rtn_oneStopOnewayTrip_lists, "directOnewayTrip_lists": rtn_directOnewayTrip_lists})

def flightInfo(request):

    BOOKING_FEE_RATE = 0.02

    request.session['num_of_stops'] = request.GET.get('num_of_stops')
    if request.session['trip'] == 'oneway' and request.session['num_of_stops'] == '0':
        directOnewayTrip_lists = cache.get('directOnewayTrip_lists')
        table_index = int(request.GET.get('table_index'))
        cache.set('order_direct_flight',directOnewayTrip_lists[table_index])
        order_direct_flight = cache.get('order_direct_flight')
        booking_fee = order_direct_flight[7] * int(request.session['num_of_psgs']) * BOOKING_FEE_RATE
        total_fare = order_direct_flight[7] * int(request.session['num_of_psgs']) * (1 + BOOKING_FEE_RATE)
        request.session['booking_fee'] = booking_fee
        request.session['total_fare'] = total_fare
        return render(request, 'mysite/flight-information.html', {"table": order_direct_flight})

    elif request.session['trip'] == 'oneway' and request.session['num_of_stops'] == '1':
        oneStopOnewayTrip_lists = cache.get('oneStopOnewayTrip_lists')
        table_index = int(request.GET.get('table_index'))
        cache.set('order_onestop_flight',oneStopOnewayTrip_lists[table_index])
        order_onestop_flight = cache.get('order_onestop_flight')
        booking_fee = order_onestop_flight[19] * int(request.session['num_of_psgs']) * BOOKING_FEE_RATE
        total_fare = order_onestop_flight[19] * int(request.session['num_of_psgs']) * (1 + BOOKING_FEE_RATE)
        request.session['booking_fee'] = booking_fee
        request.session['total_fare'] = total_fare
        return render(request, 'mysite/flight-information.html', {"table": order_onestop_flight})


def flightInfo_round(request):

    BOOKING_FEE_RATE = 0.02

    request.session['rtn_num_of_stops'] = request.GET.get('num_of_stops')

    if request.session['dst_num_of_stops'] == '0':
        dst_directOnewayTrip_lists = cache.get('dst_directOnewayTrip_lists')
        dst_table_index = int(request.session['dst_table_index'])
        cache.set('dst_order_flight',dst_directOnewayTrip_lists[dst_table_index])
        dst_order_flight = cache.get('dst_order_flight')
        dst_booking_fee = dst_order_flight[7] * int(request.session['num_of_psgs']) * BOOKING_FEE_RATE
        dst_total_fare = dst_order_flight[7] * int(request.session['num_of_psgs']) * (1 + BOOKING_FEE_RATE)

    else:
        dst_oneStopOnewayTrip_lists = cache.get('dst_oneStopOnewayTrip_lists')
        dst_table_index = int(request.session['dst_table_index'])
        cache.set('dst_order_flight',dst_oneStopOnewayTrip_lists[dst_table_index])
        dst_order_flight = cache.get('dst_order_flight')
        dst_booking_fee = dst_order_flight[19] * int(request.session['num_of_psgs']) * BOOKING_FEE_RATE
        dst_total_fare = dst_order_flight[19] * int(request.session['num_of_psgs']) * (1 + BOOKING_FEE_RATE)

    if request.session['rtn_num_of_stops'] == '0':
        rtn_directOnewayTrip_lists = cache.get('rtn_directOnewayTrip_lists')
        rtn_table_index = int(request.GET.get('rtn_table_index'))
        cache.set('rtn_order_flight',rtn_directOnewayTrip_lists[rtn_table_index])
        rtn_order_flight = cache.get('rtn_order_flight')
        rtn_booking_fee = rtn_order_flight[7] * int(request.session['num_of_psgs']) * BOOKING_FEE_RATE
        rtn_total_fare = rtn_order_flight[7] * int(request.session['num_of_psgs']) * (1 + BOOKING_FEE_RATE)

    else:
        rtn_oneStopOnewayTrip_lists = cache.get('rtn_oneStopOnewayTrip_lists')
        rtn_table_index = int(request.GET.get('rtn_table_index'))
        cache.set('rtn_order_flight',rtn_oneStopOnewayTrip_lists[rtn_table_index])
        rtn_order_flight = cache.get('rtn_order_flight')
        rtn_booking_fee = rtn_order_flight[19] * int(request.session['num_of_psgs']) * BOOKING_FEE_RATE
        rtn_total_fare = rtn_order_flight[19] * int(request.session['num_of_psgs']) * (1 + BOOKING_FEE_RATE)

    booking_fee = dst_booking_fee + rtn_booking_fee
    total_fare = dst_total_fare + rtn_total_fare
    request.session['booking_fee'] = booking_fee
    request.session['total_fare'] = total_fare

    return render(request, 'mysite/flight-information-round.html', {'dst_table': dst_order_flight, 'rtn_table': rtn_order_flight})

def queryOnewayTrip(city1, city2, weekday, diff_days, cabin, procName):
    cursor = connection.cursor()
    cursor.callproc(procName, [city1, city2, weekday])
    raw_onewayTrip_tuples = cursor.fetchall()
    cursor.close()
    raw_onewayTrip_lists = list(map(list, raw_onewayTrip_tuples))
    onewayTrip_lists = fareCalculator_a(raw_onewayTrip_lists, diff_days, cabin)
    return onewayTrip_lists

def bestSeller(request):
    cursor = connection.cursor()
    cursor.callproc('getBestSellers')
    bestSellers = cursor.fetchall()
    cursor.close()
    for i in bestSellers:
        print(i[0])
    return render(request, 'mysite/best-seller.html', {"bestSellers": bestSellers})

def fareCalculator_a(trip_lists, diff_days, cabin):
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

def fareCalculator_b(trip_lists, diff_days, cabin):
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
