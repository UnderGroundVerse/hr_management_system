# Generated by Django 5.0 on 2025-01-10 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Employees', '0003_alter_employee_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'managed': True},
        ),
    ]