# Generated by Django 4.0.5 on 2022-08-22 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticket_for_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
