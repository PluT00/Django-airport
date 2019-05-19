from django.db import models


class Flight(models.Model):
    STATUS_CHOISES = (
        ('Registration', 'Registration'),
        ('On the way', 'On the way'),
        ('Delayed', 'Delayed'),
        ('Canceled', 'Canceled'),
        ('Arrived', 'Arrived'),
        ('Departure', 'Departure')
    )
    departure_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    flight_id = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    arrival_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    company = models.CharField(max_length=50)
    plane_name = models.ForeignKey(
        'Plane',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOISES,
        default='Registration'
    )
    is_departure = models.BooleanField(default=True)

    def __str__(self):
        return self.flight_id

    class Meta:
        ordering = ['-departure_time']


class Plane(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
