# Generated by Django 2.2.5 on 2020-03-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0053_auto_20200311_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationsubscription',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='donationsubscription',
            name='success',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='9RQYEYV19TIGE75ILQ8BVPGAZFL0T5F9IYCS90OQ9291M8DQ8J3XWMH8E8NK4F0P', max_length=100),
        ),
    ]
