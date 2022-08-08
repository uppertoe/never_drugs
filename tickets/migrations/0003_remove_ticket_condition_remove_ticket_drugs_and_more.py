# Generated by Django 4.0.5 on 2022-08-08 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticket_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='drugs',
        ),
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(default='gregerg', max_length=255, verbose_name='Condition or drug to add'),
            preserve_default=False,
        ),
    ]