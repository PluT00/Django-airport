from django.test import TestCase
from django.utils import timezone

from crm.models import Flight, Plane, Ticket
from django.contrib.auth.models import User


class FlightModelTestCase(TestCase):

    def setUp(self):
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

    def test_direction_time_auto_now(self):
        auto_now = self.flight._meta.get_field('departure_time').auto_now
        self.assertEqual(auto_now, False)

    def test_direction_time_auto_now_add(self):
        auto_now_a = self.flight._meta.get_field('departure_time').auto_now_add
        self.assertEqual(auto_now_a, False)

    def test_arrival_time_auto_now(self):
        auto_now = self.flight._meta.get_field('arrival_time').auto_now
        self.assertEqual(auto_now, False)

    def test_arrival_time_auto_now_add(self):
        auto_now_add = self.flight._meta.get_field('arrival_time').auto_now_add
        self.assertEqual(auto_now_add, False)

    def test_flight_id_max_length(self):
        max_length = self.flight._meta.get_field('flight_id').max_length
        self.assertEqual(max_length, 10)

    def test_flight_id_unique(self):
        unique = self.flight._meta.get_field('flight_id').unique
        self.assertEqual(unique, True)

    def test_country_max_length(self):
        max_length = self.flight._meta.get_field('country').max_length
        self.assertEqual(max_length, 100)

    def test_city_max_length(self):
        max_length = self.flight._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)

    def test_company_max_length(self):
        max_length = self.flight._meta.get_field('company').max_length
        self.assertEqual(max_length, 50)

    def test_plane_name_related_model(self):
        related_model = self.flight._meta.get_field('plane_name').related_model
        self.assertEqual(related_model, Plane)

    def test_status_max_length(self):
        max_length = self.flight._meta.get_field('status').max_length
        self.assertEqual(max_length, 12)

    def test_status_choices(self):
        STATUS_CHOISES = (
            ('Registration', 'Registration'),
            ('On the way', 'On the way'),
            ('Delayed', 'Delayed'),
            ('Canceled', 'Canceled'),
            ('Arrived', 'Arrived'),
            ('Departure', 'Departure')
        )
        choices = self.flight._meta.get_field('status').choices
        self.assertEqual(choices, STATUS_CHOISES)

    def test_status_default(self):
        default = self.flight._meta.get_field('status').default
        self.assertEqual(default, 'Registration')

    def test_is_departure_default(self):
        default = self.flight._meta.get_field('is_departure').default
        self.assertEqual(default, True)

    def test_slug_max_length(self):
        max_length = self.flight._meta.get_field('slug').max_length
        self.assertEqual(max_length, 10)

    def test_slug_unique(self):
        unique = self.flight._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_slug_blank(self):
        blank = self.flight._meta.get_field('slug').blank
        self.assertEqual(blank, True)

    def test_slug_null(self):
        null = self.flight._meta.get_field('slug').null
        self.assertEqual(null, False)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.flight.get_absolute_url(),
            '/flight/{}/'.format(self.flight.slug)
        )

    def test_get_create_ticket_url(self):
        self.assertEqual(
            self.flight.get_create_ticket_url(),
            '/flight/{}/ticket/create/'.format(self.flight.slug)
        )

    def test_slug__str__(self):
        self.assertEqual(self.flight.__str__(), self.flight.flight_id)


class PlaneModelTestCase(TestCase):

    def setUp(self):
        self.plane = Plane.objects.create(name="A333")

    def test_name_max_length(self):
        max_length = self.plane._meta.get_field('name').max_length
        self.assertEqual(max_length, 10)

    def test_seats_default(self):
        default = self.plane._meta.get_field('seats').default
        self.assertEqual(default, 120)

    def test__str__(self):
        self.assertEqual(self.plane.__str__(), self.plane.name)


class TicketModelTestCase(TestCase):

    def setUp(self):
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
        self.user = User.objects.create_user(username="someone", password="111")
        self.ticket = Ticket.objects.create(user=self.user, flight=self.flight)

    def test_flight_related_model(self):
        related_model = self.ticket._meta.get_field('flight').related_model
        self.assertEqual(related_model, Flight)
