# Generated by Django 2.2.5 on 2020-02-02 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0023_auto_20200202_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='UNP8PVY0IA5MHCDT0GXX1UGVTQCHCP3G2H77ZTHHDKVGEGAZBOKW76NYYXD8H9RK', max_length=100),
        ),
    ]
