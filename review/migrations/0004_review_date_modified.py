# Generated by Django 4.0.5 on 2022-11-26 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_review_update_reviewsession_last_ajax_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
