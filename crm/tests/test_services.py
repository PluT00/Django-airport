from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from crm import services
from crm.models import Flight, Plane, Ticket


class FlightServicesTestCase(TestCase):
    def setUp(self):
        self.plane = Plane.objects.create(name="A333", seats=120)
        self.arrival = Flight.objects.create(
            departure_time = timezone.now(),
            flight_id = "AV 2341",
            country = "Russia",
            city = "Moscow",
            arrival_time = timezone.now(),
            company = "S7",
            plane_name = self.plane,
            status = "Registration",
            is_departure=False
        )
        self.departure = Flight.objects.create(
            departure_time = timezone.now(),
            flight_id = "AV 2342",
            country = "Russia",
            city = "Moscow",
            arrival_time = timezone.now(),
            company = "S7",
            plane_name = self.plane,
            status = "Registration",
            is_departure=True
        )

    def test_get_arrivals_and_departures_from_flights_list(self):
        arrivals, departures = services.\
            get_arrivals_and_departures_from_flights_list()

        self.assertEqual(arrivals[0], self.arrival)
        self.assertEqual(departures[0], self.departure)

    def test_get_flight_and_free_seats(self):
        user = User.objects.create_user(username='testuser', password='111')
        ticket = Ticket.objects.create(
            user=user,
            flight=self.arrival
        )
        flight, free_seats = services.get_flight_and_free_seats(self.arrival.slug)

        self.assertEqual(flight, self.arrival)
        self.assertEqual(free_seats, 119)


class TicketServicesTestCase(TestCase):
    def setUp(self):
        self.plane = Plane.objects.create(name="A333")
        self.arrival = Flight.objects.create(
            departure_time = timezone.now(),
            flight_id = "AV 2341",
            country = "Russia",
            city = "Moscow",
            arrival_time = timezone.now(),
            company = "S7",
            plane_name = self.plane,
            status = "Registration",
            is_departure=False
        )
        self.departure = Flight.objects.create(
            departure_time = timezone.now(),
            flight_id = "AV 2342",
            country = "Russia",
            city = "Moscow",
            arrival_time = timezone.now(),
            company = "S7",
            plane_name = self.plane,
            status = "Registration",
            is_departure=True
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='111'
        )
        self.arrival_ticket = Ticket.objects.create(
            user=self.user,
            flight=self.arrival
        )
        self.departure_ticket = Ticket.objects.create(
            user=self.user,
            flight=self.departure
        )

    def test_check_for_free_seats_and_post_ticket(self):
        services.check_for_free_seats_and_post_ticket(
            self.user,
            self.arrival.slug
        )
        posted_ticket = Ticket.objects.all()[2]

        self.assertEqual(posted_ticket.user, self.user)
        self.assertEqual(posted_ticket.flight, self.arrival)

    def test_delete_ticket_for_current_user_and_flight(self):
        services.delete_ticket_for_current_user_and_flight(
            self.user,
            self.arrival.slug
        )
        tickets_count = Ticket.objects.all().count()

        self.assertEqual(tickets_count, 1)

    def test_get_arrivals_and_departures_from_tickets_list(self):
        arrivals, departures = services.\
            get_arrivals_and_departures_from_tickets_list(self.user)

        self.assertEqual(arrivals[0], self.arrival_ticket)
        self.assertEqual(departures[0], self.departure_ticket)
