from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views import View

from crm.models import Flight, Ticket
from crm import services


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
        flight = Flight.objects.get(slug=slug)
        return render(
            request,
            'crm/ticket_booking.html',
            context={
                'flight': flight
            }
        )

    def post(self, request, slug):
        services.check_for_free_seats_and_post_ticket(self.request.user, slug)
        return redirect('flights_list_url')


class FlightTicketDelete(View):

    def get(self, request, slug):
        flight = Flight.objects.get(slug=slug)
        return render(
            request,
            'crm/ticket_delete.html',
            context={
                'flight': flight
            }
        )

    def post(self, request, slug):
        services.delete_ticket_for_current_user_and_flight(
            self.request.user,
            slug
        )
        return redirect('flights_list_url')


class MyTickets(View):

    def get(self, request):
        if self.request.user.is_authenticated:
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
        else:
            return render(request, '404.html')
