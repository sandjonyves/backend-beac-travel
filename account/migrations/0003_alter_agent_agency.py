# Generated by Django 5.0.4 on 2024-12-21 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_delete_admin_delete_agent_delete_superuser_superuser_and_more'),
        ('app', '0003_remove_agency_agencymanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='agency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='app.agency'),
        ),
    ]
