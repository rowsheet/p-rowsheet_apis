# Generated by Django 2.2.5 on 2020-01-10 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0006_pronoun'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='pronoun',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='rideshare.Pronoun'),
        ),
    ]