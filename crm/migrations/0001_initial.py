# Generated by Django 3.1 on 2020-08-25 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('flight_id', models.CharField(max_length=10, unique=True)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('arrival_time', models.DateTimeField()),
                ('company', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Registration', 'Registration'), ('On the way', 'On the way'), ('Delayed', 'Delayed'), ('Canceled', 'Canceled'), ('Arrived', 'Arrived'), ('Departure', 'Departure')], default='Registration', max_length=12)),
                ('is_departure', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=10, unique=True)),
            ],
            options={
                'ordering': ['-departure_time'],
            },
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('seats', models.IntegerField(default=120)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.flight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='plane_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.plane'),
        ),
    ]
