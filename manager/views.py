from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def action(request):
    if request.method == 'POST':
        action = request.POST['actionSelect']
        print(action)
        if 'Manage Customer Accounts' == action:
            return redirect('/admin/auth/user/')
        elif 'Manage Reservations' == action:
            return redirect('manage_reservations')
        elif 'View All Flight Information' == action:
            return redirect('/admin/mysite/route/')
        elif 'Generate Sales Reports' == action:
            return redirect('generate_sales_reports')
        elif 'Get Best Customer' == action:
            return redirect('get_best_customer')
        elif 'List All Flights for a Given Airport' == action:
            return redirect('list_flights_for_a_airport')
        else:
            return redirect('/admin')
    else:
        return redirect('/admin')

# Create your views here.
def manage_customers(request):
    context={
        'title': 'Manage Customers'
    }
    return render(request,"admin/manage_customers.html",context=context)

def manage_reservations(request):
    if request.method == 'GET':
        reservation_tuples = None
        search_type = None
        if 'last_name' in request.GET:
            search_type = 'last_name'
            last_name = request.GET.get('last_name')
            cursor = connection.cursor()
            cursor.callproc('getReservationsbyUser', [last_name])
            reservation_tuples = cursor.fetchall()
            cursor.close()


        elif 'flight_no' in request.GET:
            search_type = 'flight_no'
            flight_no = request.GET.get('flight_no')
            cursor = connection.cursor()
            cursor.callproc('getReservationsbyFlight', [flight_no])
            reservation_tuples = cursor.fetchall()
            cursor.close()

        context={
                    'title': 'Manage Reservations',
                    'reservation_tuples': reservation_tuples,
                    'search_type': search_type
            }

        return render(request,"admin/manage_reservations.html",context=context)



    return render(request,"admin/manage_reservations.html")





def view_flights(request):
    context={
        'title': 'View Flights'
    }
    return render(request,"admin/flights.html",context=context)

def generate_sales_reports(request):
    if request.method == 'GET':
        sales_tuples = None
        search_type = None
        if request.GET.get('search') == 'by_flight':
            search_type = 'by_flight'
            cursor = connection.cursor()
            cursor.callproc('getSummaryByFlight')
            sales_tuples = cursor.fetchall()
            cursor.close()
            print('sssssss')


        elif request.GET.get('search') == 'by_dst_city':
            search_type = 'by_dst_city'
            cursor = connection.cursor()
            cursor.callproc('getSummaryByCity')
            sales_tuples = cursor.fetchall()
            cursor.close()

        elif request.GET.get('search') == 'by_customer':
            search_type = 'by_customer'
            cursor = connection.cursor()
            cursor.callproc('getSummaryByCustomer')
            sales_tuples = cursor.fetchall()
            cursor.close()

        context={
                    'title': 'Sales Report',
                    'sales_tuples': sales_tuples,
                    'search_type': search_type
            }


        return render(request,"admin/reporting.html",context=context)

    return render(request,"admin/reporting.html")

def get_best_customer(request):

    cursor = connection.cursor()
    cursor.callproc('getBestCustomer')
    tuples = cursor.fetchall()
    cursor.close()


    context={
        'title': 'Our Best Customer',
        'tuples': tuples
    }

    return render(request,"admin/get_best_customer.html",context=context)


def list_flights_for_a_airport(request):
    if request.method == 'GET':
        tuples = None
        airport_id = request.GET.get('search')
        cursor = connection.cursor()
        cursor.callproc('getFlightsAtAirport',[airport_id])
        tuples = cursor.fetchall()
        cursor.close()


        context={
        'title': 'List Flights at a Aiport',
        'tuples': tuples
        }

        return render(request,"admin/flights_at_airport.html",context=context)

    return render(request,"admin/flights_at_airport.html")
