# Generated by Django 5.1.4 on 2024-12-22 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_mission_status_alter_trip_mission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agencies', to='app.service'),
        ),
    ]