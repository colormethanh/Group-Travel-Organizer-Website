# Generated by Django 4.0.4 on 2022-05-11 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_group_remove_comment_trip_remove_event_trip_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='group',
            name='start_date',
        ),
    ]
