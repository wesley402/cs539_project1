from django.contrib import admin
from django.db import connection
from .models import Reservation, Leg

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()],columns

# Register your models here.
class ReservationAdmin(admin.ModelAdmin):
  with connection.cursor() as cursor:
    cursor.execute('select * from orders_reservation;')
    q, fields = dictfetchall(cursor)
    list_display = fields
    list_filter = (
      'reservation_date',
      'reservation_status',
      'num_legs',
      'total_fare',
    )
    # search_fields = ['user__last_name']


admin.site.register(Reservation, ReservationAdmin)