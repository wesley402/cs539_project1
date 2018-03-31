from django.shortcuts import render

# Create your views here.
def manage_customers(request):
    context = {'user': request.user}
    # if request.POST == 'Manage Customer Accounts':
    return render(request,"admin/customers.html",context=context)