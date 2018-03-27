from django.shortcuts import render
from accounts.models import Profile

from django.contrib.auth.models import User
from django.db import connection


# Create your views here.
def dashboard(request):
    context = {'user': request.user}
    return render(request, "dashboard/dashboard.html",context=context)
    
def customer(request):
    users = Profile.objects.all()
    context = {
        "users":users
    }
    return render(request, "dashboard/customers.html",context=context)

def flight(request):
    with connection.cursor() as cursor:
        cursor.callproc('getAllFlights')
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(result[0:])
        context = {
            "flights":result[:100]
        }
    return render(request, "dashboard/flights.html",context=context)

def reservation(request):
    return render(request, "dashboard/reservations.html")
 
# def my_custom_sql(self):
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM accounts_account where id=%s",[self.id])
#     row = cursor.fetchall()
#     return row

# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]