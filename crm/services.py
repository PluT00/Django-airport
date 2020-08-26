from django.shortcuts import get_object_or_404

from crm.models import Flight, Ticket


def get_arrivals_and_departures_from_flights_list():
    arrivals = []
    departures = []
    flights = Flight.objects.all()
    for flight in flights:
        if flight.is_departure:
            departures.append(flight)
        else:
            arrivals.append(flight)

    return arrivals, departures

def get_flight_and_free_seats(slug):
    flight = get_object_or_404(Flight, slug=slug)
    tickets = Ticket.objects.filter(flight=flight).count()
    free_seats = flight.plane_name.seats - tickets

    return flight, free_seats

def check_for_free_seats_and_post_ticket(current_user, slug):
    current_flight = get_object_or_404(Flight, slug=slug)
    tickets = Ticket.objects.filter(flight=current_flight).count()
    seats = current_flight.plane_name.seats
    if tickets < seats:
        new_ticket = Ticket.objects.create(
            user=current_user,
            flight=current_flight
        )

def delete_ticket_for_current_user_and_flight(current_user, slug):
    current_user=current_user
    current_flight = get_object_or_404(Flight, slug=slug)
    tickets = Ticket.objects.filter(flight=current_flight, user=current_user)
    tickets[0].delete()

def get_arrivals_and_departures_from_tickets_list(current_user):
    arrivals = []
    departures = []
    tickets = Ticket.objects.filter(user=current_user)
    for ticket in tickets:
        if ticket.flight.is_departure:
            departures.append(ticket)
        else:
            arrivals.append(ticket)

    return arrivals, departures
