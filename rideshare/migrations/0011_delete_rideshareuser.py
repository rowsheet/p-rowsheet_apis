# Generated by Django 2.2.5 on 2020-01-22 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0010_rideshareuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RideshareUser',
        ),
    ]
