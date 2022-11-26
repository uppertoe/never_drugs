# Generated by Django 4.0.5 on 2022-11-26 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0019_condition_peer_review_status_and_more'),
        ('review', '0005_remove_review_interaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='condition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Condition', to='reactions.condition'),
        ),
    ]
