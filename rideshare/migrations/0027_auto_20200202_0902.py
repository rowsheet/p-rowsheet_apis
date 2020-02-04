# Generated by Django 2.2.5 on 2020-02-02 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0026_auto_20200202_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='LEF5N5J9VWJ39DJ1S9UOCGG0CIIIV74BDJZQPLXD7JAIORX6G582AGYJUE0P7A7P', max_length=100),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='app_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='rideshare.AppUser', unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='riderequest',
            unique_together=set(),
        ),
    ]
