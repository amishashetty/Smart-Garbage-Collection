# Generated by Django 4.0.2 on 2022-09-13 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garbageapp', '0014_bin_status_trackinghistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackinghistory',
            name='complain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='garbageapp.complain'),
        ),
    ]