# Generated by Django 2.2.5 on 2020-03-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0064_auto_20200317_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='estimated_duration',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='suggested_donation',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='total_distance',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='Y80IKCJNKZ4YNV5KQAKRHAWXCO6N25L4D53NT12CXDVFQLCE7MWG10HGCNRVJ476', max_length=100),
        ),
    ]
