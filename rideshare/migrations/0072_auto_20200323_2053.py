# Generated by Django 2.2.3 on 2020-03-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0071_merge_20200322_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='M2348YU07PGU89K3WQ6LYI5WQRQ2N0X1E6U6B12NNZPHD783NV2P8QBSE25J36DD', max_length=100),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='color_code',
            field=models.CharField(blank=True, choices=[('RED', 'RED'), ('YELLOW', 'YELLOW'), ('ORANGE', 'ORANGE'), ('GREEN', 'GREEN'), ('BLUE', 'BLUE')], default=None, max_length=32, null=True),
        ),
    ]