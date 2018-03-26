from django.shortcuts import render
from accounts.models import Profile

from django.contrib.auth.models import User


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
    return render(request, "dashboard/flights.html")

def reservation(request):
    return render(request, "dashboard/reservations.html")
