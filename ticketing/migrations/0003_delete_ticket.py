# Generated by Django 3.1.2 on 2020-12-16 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_remove_movie_genre'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
