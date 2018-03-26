"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from . import views as home_views
from django.views.generic import TemplateView
from accounts import views as accounts_views
from orders import views as orders_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('admin/', admin.site.urls),

    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/customer', dashboard_views.customer, name='customer'),
    path('dashboard/flight', dashboard_views.flight, name='flight'),
    path('dashboard/reservation', dashboard_views.reservation, name='reservation'),

    path('signin/',accounts_views.signin, name = 'signin'),
    path('signup/',accounts_views.signup, name = 'signup'),
    path('signout/',accounts_views.signout, name = 'signout'),
    path('profile/', accounts_views.profile, name='profile'),
    path('profile/edit', accounts_views.edit_profile, name='edit_profile'),

    path('flight-search/', home_views.searchResults, name='flight-search'),
    path('flight-information/', home_views.flightInfo, name='flight-information'),
    path('best-seller/', home_views.bestSeller, name='best-seller'),

    path('checkout/', orders_views.checkout, name='checkout'),
    path('order/', orders_views.order, name='order'),
    path('order/history-order', orders_views.order, name='history_order'),
    path('order/current-order', orders_views.order, name='current_order'),

]
