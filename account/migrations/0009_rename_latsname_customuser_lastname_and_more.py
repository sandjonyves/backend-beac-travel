# Generated by Django 5.1.4 on 2024-12-23 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_customuser_admin_id_customuser_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='latsName',
            new_name='lastName',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]