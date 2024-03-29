# Generated by Django 2.2.5 on 2020-02-04 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rideshare', '0031_auto_20200204_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='OldRideRequest',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='OldRideRequest',
            name='driver',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='TWCNJB68UYOT2UZMMGPNVUVPVI8V0P2J6MX09QG6Y6JS42KM3LY8XDW872DGGQTT', max_length=100),
        ),
    ]
