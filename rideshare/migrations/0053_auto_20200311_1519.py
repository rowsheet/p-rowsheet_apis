# Generated by Django 2.2.5 on 2020-03-11 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0052_auto_20200311_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email_verification_code',
            field=models.CharField(default='6JN1NJTJ4NTKKMMM85EN7CE872TDL6PHV88QGF6UFDN9SBAFN4JJ0Q0FSNHN426A', max_length=100),
        ),
        migrations.CreateModel(
            name='DonationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.CharField(max_length=500)),
                ('checkout_session_id', models.CharField(max_length=500)),
                ('amount', models.FloatField(blank=True, default=None, null=True)),
                ('app_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='rideshare.AppUser')),
            ],
        ),
    ]
