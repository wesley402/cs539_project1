from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from . import views as home_views
from django.views.generic import TemplateView
from accounts import views as accounts_views
from orders import views as orders_views
# from myadmin import views as myadmin_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    
    path('admin/action/', home_views.action, name="action"),
    path('admin/manage_customers/', home_views.manage_customers, name="manage_customers"),
    path('admin/manage_reservations/', home_views.manage_reservations, name='manage_reservations'),
    path('admin/view_flights/', home_views.view_flights, name='flights'),
    path('admin/reports/', home_views.generate_reports, name='reports'),

    path('signin/',accounts_views.signin, name = 'signin'),
    path('signup/',accounts_views.signup, name = 'signup'),
    path('signout/',accounts_views.signout, name = 'signout'),
    path('profile/', accounts_views.profile, name='profile'),
    path('profile/edit', accounts_views.edit_profile, name='edit_profile'),

    path('flight-search-dst/', home_views.searchResults, name='flight-search-dst'),
    path('flight-search-rtn/', home_views.searchResults_rtn, name='flight-search-rtn'),

    path('flight-information-round/', home_views.flightInfo_round, name='flight-information-round'),

    path('flight-information/', home_views.flightInfo, name='flight-information'),
    path('best-seller/', home_views.bestSeller, name='best-seller'),

    path('checkout/', orders_views.checkout, name='checkout'),
    path('order/', orders_views.order, name='order'),
    path('order/history-order', orders_views.history_order, name='history_order'),
    path('order/current-order', orders_views.current_order, name='current_order'),
    #path('order/order-detail', orders_views.order_detail, name='order_detail'),

]
