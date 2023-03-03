# Generated by Django 4.1.7 on 2023-03-03 00:08

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0024_condition_tldr_condition_tldr_box_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='see_also',
            field=models.ManyToManyField(blank=True, to='reactions.condition'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='tldr',
            field=markdownx.models.MarkdownxField(blank=True, help_text='A brief description of the important anaesthetic concern to appear at the top of the article', null=True, verbose_name='TL;DR'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='tldr_box',
            field=models.CharField(choices=[('GY', 'Grey'), ('BL', 'Blue'), ('YE', 'Yellow'), ('GN', 'Green'), ('RE', 'Red')], default='RE', max_length=2, verbose_name='TL;DR banner colour'),
        ),
    ]
