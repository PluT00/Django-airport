from django.contrib import admin
from crm.models import Flight, Plane


class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_id',
        'departure_time',
        'company',
        'plane_name',
        'is_departure',
        'status'
    ]
    search_fields = [
        'flight_id',
        'company',
        'status'
    ]

admin.site.register(Flight, FlightAdmin)


class PlaneAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Plane, PlaneAdmin)
