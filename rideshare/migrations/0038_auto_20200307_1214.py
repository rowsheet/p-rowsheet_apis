# Generated by Django 2.2.3 on 2020-03-07 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0037_auto_20200307_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='69YYNOHOR4X0QYVLXGXBD99GDUGXMSAFZQRPBEW0QORIZLVF1EMJCAKW6H80G56A', max_length=100),
        ),
        migrations.AlterField(
            model_name='olddriversignup',
            name='contact_phone',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oldriderequest',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]