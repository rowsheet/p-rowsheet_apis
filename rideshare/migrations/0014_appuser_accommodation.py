# Generated by Django 2.2.5 on 2020-01-23 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0013_accommodation'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='accommodation',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='rideshare.Accommodation'),
        ),
    ]
