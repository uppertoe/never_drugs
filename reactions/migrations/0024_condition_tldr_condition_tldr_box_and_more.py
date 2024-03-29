# Generated by Django 4.1.7 on 2023-03-01 01:33

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0023_alter_condition_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='tldr',
            field=markdownx.models.MarkdownxField(blank=True, help_text='A brief description of the important anaesthetic concernsto appear at the top of the article', null=True, verbose_name='TL;DR'),
        ),
        migrations.AddField(
            model_name='condition',
            name='tldr_box',
            field=models.CharField(choices=[('GY', 'Grey'), ('BL', 'Blue'), ('YE', 'Yellow'), ('GN', 'Green'), ('RE', 'Red')], default='RE', max_length=2),
        ),
        migrations.AlterField(
            model_name='condition',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, default='# Overview\n---\nOverview text here\n\n# Pathophysiology\n---\nPathophysiology text here\n\n# Impacts on anaesthesia\n---\nImpacts text here \n\n### *Drug name here*\n`Expert opinion` Further detail here', help_text='Add basic formatting using <a href="https://www.markdownguide.org/cheat-sheet/" target="_blank" rel="noopener noreferrer">Markdown (cheat sheet)</a><br>A live preview of formatted content     is shown next to the input field', null=True, verbose_name='Article body'),
        ),
    ]
