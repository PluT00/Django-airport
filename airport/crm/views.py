from django.shortcuts import render
from django.shortcuts import get_object_or_404

from crm.models import Flight


def flights_list(request):
    arrivals = []
    departures = []
    flights = Flight.objects.all()
    for flight in flights:
        if flight.is_departure:
            departures.append(flight)
        else:
            arrivals.append(flight)
    return render(request,
        'crm/flights_list.html',
        context={
            'departures': departures,
            'arrivals': arrivals
        }
    )


def flight_details(request, slug):
    flight = get_object_or_404(Flight, slug__iexact=slug)
    return render(request,
        'crm/flight_details.html',
        context={
            'flight': flight
        }
    )
