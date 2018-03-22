from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext, loader
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import Route
from django.core.cache import cache
import datetime
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
        dep_date = request.GET.get('dep_date')
        weekday = datetime.datetime.strptime(dep_date, '%m/%d/%Y').strftime('%a')

        request.session['nums_of_psgs'] = nums_of_psgs
        query_tables = Route.objects.raw('SELECT * FROM mysite_route WHERE src_airport=%s AND dst_airport = %s',[city1, city2])
        cache.set('query_tables',query_tables)
        return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

    elif(search_type == 'roundtrip'):
        return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

    elif(search_type == 'multicity'):
        return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

    return render(request, 'mysite/flight-search.html', {"query_tables": query_tables})

def flightInfo(request):
    table_index = int(request.GET.get('table_index'))
    query_tables = cache.get('query_tables')
    #print(query_tables[0])

    return render(request, 'mysite/flight-information.html', {"order": query_tables[table_index]})

def bestSeller(request):
    return render(request, 'mysite/best-seller.html')
