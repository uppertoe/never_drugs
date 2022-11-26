# Generated by Django 4.0.5 on 2022-11-26 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0019_condition_peer_review_status_and_more'),
        ('review', '0004_review_date_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='interaction',
        ),
        migrations.RemoveField(
            model_name='reviewsession',
            name='interaction_reviews',
        ),
        migrations.AddField(
            model_name='review',
            name='condition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Condition', to='reactions.condition'),
        ),
        migrations.AddField(
            model_name='reviewsession',
            name='reviews',
            field=models.ManyToManyField(blank=True, related_name='reviews', to='review.review', verbose_name='Articles for peer review'),
        ),
    ]