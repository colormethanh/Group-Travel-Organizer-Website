# Generated by Django 4.0.4 on 2022-05-02 06:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_going_trip_members_going_trip_going_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='key',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(3, 'Trip title must be longer than 3 characters')]),
        ),
    ]