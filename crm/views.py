from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from crm import services
from crm.models import Flight, Ticket


def flights_list(request):
    arrivals, departures = services.\
        get_arrivals_and_departures_from_flights_list()
    return render(request,
        'crm/flights_list.html',
        context={
            'departures': departures,
            'arrivals': arrivals
        }
    )


def flight_details(request, slug):
    flight, free_seats = services.get_flight_and_free_seats(slug)
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
        flight = get_object_or_404(Flight, slug=slug)
        return render(
            request,
            'crm/ticket_booking.html',
            context={
                'flight': flight
            }
        )

    def post(self, request, slug):
        try:
            services.check_for_free_seats_and_post_ticket(self.request.user, slug)
            return redirect('flights_list_url')
        except ValueError:
            return HttpResponse(status=400)


class FlightTicketDelete(View):

    def get(self, request, slug):
        flight = get_object_or_404(Flight, slug=slug)
        return render(
            request,
            'crm/ticket_delete.html',
            context={
                'flight': flight
            }
        )

    def post(self, request, slug):
        try:
            services.delete_ticket_for_current_user_and_flight(
                self.request.user,
                slug
            )
            return redirect('flights_list_url')
        except TypeError:
            return HttpResponse(status=400)


class MyTickets(View):

    def get(self, request):
        try:
            arrivals, departures = services.\
                get_arrivals_and_departures_from_tickets_list(self.request.user)
            return render(
                request,
                'crm/my_tickets.html',
                context={
                    'departures': departures,
                    'arrivals': arrivals
                }
            )
        except TypeError:
            return HttpResponse(status=400)
