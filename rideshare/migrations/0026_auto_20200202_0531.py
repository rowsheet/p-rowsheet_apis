# Generated by Django 2.2.5 on 2020-02-02 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0025_auto_20200202_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='A5AWYFJABITYAULECQY9W8IWDPJD9IIX9AWRQ7C4PIXZUK8SZK3Y0GLNZ2Z9K7FC', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='riderequest',
            unique_together={('app_user', 'status')},
        ),
    ]