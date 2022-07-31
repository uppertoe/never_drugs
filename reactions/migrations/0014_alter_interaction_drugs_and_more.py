# Generated by Django 4.0.5 on 2022-07-31 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0013_interaction_secondary_drugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='drugs',
            field=models.ManyToManyField(blank=True, related_name='interactions', to='reactions.drug', verbose_name='Contraindicated drugs'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='secondary_drugs',
            field=models.ManyToManyField(blank=True, related_name='secondary_interactions', to='reactions.drug', verbose_name='Drugs to use with caution'),
        ),
    ]
