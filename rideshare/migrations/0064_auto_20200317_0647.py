# Generated by Django 2.2.5 on 2020-03-17 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0063_auto_20200317_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='ridedonation',
            name='ride_request',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='rideshare.RideRequest'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='DNTEQVOUH2QHKIL0QD6ASGIXGKOEG8VENQU826FPXA14EG1VDCW67Q0BXRNSAU3P', max_length=100),
        ),
    ]