# Generated by Django 4.0.5 on 2022-11-26 10:52

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0020_remove_interaction_evidence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
