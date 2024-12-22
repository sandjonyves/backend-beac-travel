# Generated by Django 5.0.4 on 2024-12-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_superuser_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='firstName',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='latsName',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
