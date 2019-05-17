from django.test import TestCase
from django.utils import timezone

from crm.models import Flight, Plane


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
            status = "RG"
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
        self.assertEqual(max_length, 2)

    def test_status_choices(self):
        STATUS_CHOISES = (
            ('RG', 'Registration'),
            ('OW', 'On the way'),
            ('DL', 'Delayed'),
            ('CN', 'Canceled'),
            ('AR', 'Arrived'),
            ('DP', 'Departure')
        )
        choices = self.flight._meta.get_field('status').choices
        self.assertEqual(choices, STATUS_CHOISES)

    def test_status_default(self):
        default = self.flight._meta.get_field('status').default
        self.assertEqual(default, 'RG')

    def test_is_departure_default(self):
        default = self.flight._meta.get_field('is_departure').default
        self.assertEqual(default, True)


class PlaneModelTestCase(TestCase):

    def setUp(self):
        self.plane = Plane.objects.create(name="A333")

    def test_name_max_length(self):
        max_length = self.plane._meta.get_field('name').max_length
        self.assertEqual(max_length, 10)
