# Generated by Django 2.2.5 on 2020-02-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0029_auto_20200204_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='47HACUNZCO863E1PIR397MII84YNE2AB14TNR8ARPY9U5Q4UI7DT44OP95S2JWH7', max_length=100),
        ),
        migrations.AlterField(
            model_name='oldriderequest',
            name='pickup_time',
            field=models.TimeField(default=None),
        ),
    ]
