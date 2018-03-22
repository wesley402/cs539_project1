from django.shortcuts import render

# Create your views here.
def checkout(request):
    nums_of_psgs = int(request.session['nums_of_psgs'])
    return render(request, 'orders/checkout.html', {'range':range(nums_of_psgs)})

def order(request):
    return render(request, 'orders/order.html')
