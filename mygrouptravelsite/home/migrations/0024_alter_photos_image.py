# Generated by Django 4.0.4 on 2022-05-10 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_photos_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='image',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]