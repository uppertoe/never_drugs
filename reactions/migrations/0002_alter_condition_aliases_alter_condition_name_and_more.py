# Generated by Django 4.0.5 on 2022-07-10 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='aliases',
            field=models.CharField(blank=True, max_length=1023),
        ),
        migrations.AlterField(
            model_name='condition',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='aliases',
            field=models.CharField(blank=True, max_length=1023),
        ),
        migrations.AlterField(
            model_name='drug',
            name='drug_class',
            field=models.ManyToManyField(blank=True, to='reactions.drugclass'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='drugclass',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='reaction_type',
            field=models.CharField(max_length=255),
        ),
    ]
