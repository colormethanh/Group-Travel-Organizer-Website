# Generated by Django 4.0.4 on 2022-05-11 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_photos_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='description',
            field=models.TextField(default='A cool trip for a cool group of people :)', max_length=200),
        ),
    ]
