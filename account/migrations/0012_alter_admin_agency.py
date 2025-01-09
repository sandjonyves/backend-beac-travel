# Generated by Django 5.1.4 on 2025-01-09 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_admin_agency'),
        ('app', '0009_alter_agency_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='agency',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_user', to='app.agency'),
        ),
    ]