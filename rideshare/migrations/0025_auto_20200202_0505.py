# Generated by Django 2.2.5 on 2020-02-02 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0024_auto_20200202_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING_CONFIRM', 'PENDING_CONFIRM'), ('PENDING_DRIVER', 'PENDING_DRIVER'), ('PENDING_PICKUP', 'PENDING_PICKUP'), ('PENDING_DROPOFF', 'PENDING_DROPOFF'), ('CANCELED', 'CANCELED'), ('DONE', 'DONE')], default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='FC5IJE3HTSHNYSDFICIDOU394GN0AX1Z3QSVFH8IP5U1TT0V1OQ3K85H8JG148ZA', max_length=100),
        ),
    ]
