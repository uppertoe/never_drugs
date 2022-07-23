# Generated by Django 4.0.5 on 2022-07-23 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0009_rename_source_interaction_sources'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='condition',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='drug',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='drug',
            name='drug_class',
            field=models.ManyToManyField(blank=True, related_name='drugs', to='reactions.drugclass'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='conditions',
            field=models.ManyToManyField(related_name='interactions', to='reactions.condition'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='drugs',
            field=models.ManyToManyField(related_name='interactions', to='reactions.drug'),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='sources',
            field=models.ManyToManyField(related_name='sources', to='reactions.source'),
        ),
    ]