# Generated by Django 2.2.5 on 2020-03-11 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0054_auto_20200311_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationsubscription',
            name='currency',
            field=models.CharField(blank=True, default=None, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='donationsubscription',
            name='inverval',
            field=models.CharField(blank=True, default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='X5984NTM7H6MA6ECK69IX6H0LZEI4AHP8PWCSXQF4NICGITARD1ZXEVPPJW3XZGW', max_length=100),
        ),
    ]