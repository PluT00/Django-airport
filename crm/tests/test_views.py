from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User

from crm.models import Plane, Flight, Ticket


class FlightViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.plane = Plane.objects.create(name="A333")
        self.flight = Flight.objects.create(
            departure_time = timezone.now(),
            flight_id = "AV 2341",
            country = "Russia",
            city = "Moscow",
            arrival_time = timezone.now(),
            company = "S7",
            plane_name = self.plane,
            status = "Registration"
        )

    def test_flights_list_GET(self):
        response = self.client.get(reverse('flights_list_url'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/flights_list.html')

    def test_flight_details_GET(self):
        response = self.client.get(
            reverse(
                'flight_details_url',
                kwargs={'slug': self.flight.slug}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/flight_details.html')

    def test_flight_details_GET_not_found(self):
        response = self.client.get(
            reverse(
                'flight_details_url',
                kwargs={'slug': 'test_slug'}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_details_GET_without_slug(self):
        response = self.client.get(
            reverse(
                'flight_details_url',
                kwargs={'slug': None}
            )
        )

        self.assertEqual(response.status_code, 404)


class TicketViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.plane = Plane.objects.create(name="A333")
        self.flight = Flight.objects.create(
            departure_time = timezone.now(),
            flight_id = "AV 2341",
            country = "Russia",
            city = "Moscow",
            arrival_time = timezone.now(),
            company = "S7",
            plane_name = self.plane,
            status = "Registration"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='111')
        self.ticket = Ticket.objects.create(
            user=self.user,
            flight=self.flight
        )
        self.client.login(username='testuser', password='111')

    def test_flight_ticket_GET(self):
        response = self.client.get(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': self.flight.slug}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/ticket_booking.html')

    def test_flight_ticket_GET_flight_not_flight(self):
        response = self.client.get(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': 'test_slug'}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_GET_without_slug(self):
        response = self.client.get(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': None}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_POST(self):
        response = self.client.post(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': self.flight.slug}
            )
        )
        posted_ticket = Ticket.objects.all()[1]

        self.assertEqual(response.status_code, 302)
        self.assertEqual(posted_ticket.user, self.user)
        self.assertEqual(posted_ticket.flight, self.flight)

    def test_flight_ticket_POST_flight_not_found(self):
        response = self.client.post(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': 'test_slug'}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_POST_without_slug(self):
        response = self.client.post(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': None}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_POST_as_anonymous_user(self):
        self.client.logout()
        response = self.client.post(
            reverse(
                'flight_ticket_url',
                kwargs={'slug': self.flight.slug}
            )
        )

        self.assertEqual(response.status_code, 400)

    def test_flight_ticket_delete_GET(self):
        response = self.client.get(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': self.flight.slug}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/ticket_delete.html')

    def test_flight_ticket_delete_GET_flight_not_found(self):
        response = self.client.get(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': 'test_slug'}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_delete_GET_without_slug(self):
        response = self.client.get(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': None}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_delete_POST(self):
        response = self.client.post(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': self.flight.slug}
            )
        )

        tickets_count = Ticket.objects.all().count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(tickets_count, 0)

    def test_flight_ticket_delete_POST_flight_not_found(self):
        response = self.client.post(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': 'test_slug'}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_delete_POST_without_slug(self):
        response = self.client.post(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': None}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_flight_ticket_delete_POST_as_anonymous_user(self):
        self.client.logout()
        response = self.client.post(
            reverse(
                'flight_ticket_delete_url',
                kwargs={'slug': self.flight.slug}
            )
        )

        self.assertEqual(response.status_code, 400)

    def test_my_tickets_GET(self):
        response = self.client.get(reverse('my_tickets_url'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/my_tickets.html')

    def test_my_tickets_GET_as_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('my_tickets_url'))

        self.assertEqual(response.status_code, 400)
