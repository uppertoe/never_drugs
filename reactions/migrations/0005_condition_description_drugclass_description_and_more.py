# Generated by Django 4.0.5 on 2022-07-17 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0004_rename_condition_interaction_conditions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='description',
            field=models.TextField(blank=True, max_length=1023),
        ),
        migrations.AddField(
            model_name='drugclass',
            name='description',
            field=models.TextField(blank=True, max_length=1023),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='evidence',
            field=models.CharField(choices=[('L1', 'Systematic review of RCTs'), ('L2', 'Well-designed RCT'), ('L3', 'Well-designed controlled study without randomisation'), ('L4', 'Well designed case-control or cohort studies'), ('L5', 'Reviews of qualitative studies'), ('L6', 'Single qualitative study'), ('L7', 'Expert body opinion')], default='L7', max_length=2),
        ),
    ]
