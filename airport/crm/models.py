from django.db import models


class Flight(models.Model):
    STATUS_CHOISES = (
        ('RG', 'Registration'),
        ('OW', 'On the way'),
        ('DL', 'Delayed'),
        ('CN', 'Canceled'),
        ('AR', 'Arrived'),
        ('DP', 'Departure')
    )
    departure_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    flight_id = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    arrival_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    company = models.CharField(max_length=50)
    plane_name = models.ForeignKey(
        'Plane',
        on_delete=models.CASCADE,
        related_name="flights"
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOISES,
        default='RG'
    )
    is_departure = models.BooleanField(default=True)

    def __str__(self):
        return '{0}'.format(self.flight_id)


class Plane(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return '{0}'.format(self.name)
