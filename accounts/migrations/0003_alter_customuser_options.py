# Generated by Django 4.1.7 on 2023-04-26 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('access_peer_review', 'Can access the peer review module'),), 'verbose_name': 'User'},
        ),
    ]
