# Generated by Django 4.0.2 on 2022-09-06 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garbageapp', '0006_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='user',
        ),
        migrations.AddField(
            model_name='driver',
            name='bin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='garbageapp.bin'),
        ),
    ]
