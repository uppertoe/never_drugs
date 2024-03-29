# Generated by Django 4.1.7 on 2023-03-03 05:03

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0025_condition_see_also_alter_condition_tldr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, help_text="Use this field to outline the drug's background and contraindications", null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='see_also',
            field=models.ManyToManyField(blank=True, help_text='Link to related conditions here <br>', to='reactions.condition', verbose_name='See also'),
        ),
    ]
