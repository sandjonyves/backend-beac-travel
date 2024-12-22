# Generated by Django 5.0.4 on 2024-12-22 06:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_mission_is_validated_alter_mission_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='status',
            field=models.CharField(choices=[('in creation', 'In Creation'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('in progress', 'In Progress'), ('rejected', 'Rejected'), ('failure', 'Failure'), ('finish', 'Finish')], default='in creation', max_length=20),
        ),
        migrations.AlterField(
            model_name='trip',
            name='mission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='app.mission'),
        ),
    ]
