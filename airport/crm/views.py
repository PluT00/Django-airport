from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views import View

from crm.models import Flight, Ticket


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
    tickets = Ticket.objects.filter(flight=flight).count()
    free_seats = flight.plane_name.seats - tickets
    return render(request,
        'crm/flight_details.html',
        context={
            'flight': flight,
            'free_seats': free_seats,
            'seats': flight.plane_name.seats
        }
    )


class FlightTicket(View):

    def get(self, request, slug):
        flight = Flight.objects.get(slug__iexact=slug)
        return render(
            request,
            'crm/ticket_booking.html',
            context={
                'flight': flight
            }
        )

    def post(self, request, slug):
        current_flight = Flight.objects.get(slug__iexact=slug)
        current_user = self.request.user
        tickets = Ticket.objects.filter(flight=current_flight).count()
        seats = current_flight.plane_name.seats
        if tickets < seats:
            new_ticket = Ticket.objects.create(
                user=current_user,
                flight=current_flight
            )
        return redirect('flights_list_url')
