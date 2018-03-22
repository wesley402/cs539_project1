from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "dashboard/index.html")
def customer(request):
    return render(request, "dashboard/customers.html")
def flight(request):
    return render(request, "dashboard/flights.html")
def reservation(request):
    return render(request, "dashboard/reservations.html")
