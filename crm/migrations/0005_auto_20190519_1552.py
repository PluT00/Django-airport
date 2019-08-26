# Generated by Django 2.2.1 on 2019-05-19 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20190519_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='status',
            field=models.CharField(choices=[('Registration', 'Registration'), ('On the way', 'On the way'), ('Delayed', 'Delayed'), ('Canceled', 'Canceled'), ('Arrived', 'Arrived'), ('Departure', 'Departure')], default='Registration', max_length=12),
        ),
    ]