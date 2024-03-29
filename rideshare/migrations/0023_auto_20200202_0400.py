# Generated by Django 2.2.5 on 2020-02-02 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0022_appuser_email_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='app_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='rideshare.AppUser'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='001J5FQB893YK44NTKD6WZ9PHQ0F5FIGCIC4H1D105LO345JBKOXSH4OOQUR652P', max_length=100),
        ),
    ]
