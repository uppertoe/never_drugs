# Generated by Django 4.0.5 on 2022-07-18 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0008_source_interaction_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interaction',
            old_name='source',
            new_name='sources',
        ),
    ]