# Generated by Django 5.0.2 on 2024-03-07 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_management', '0017_alter_department_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Company',
            new_name='Companies',
        ),
        migrations.RenameModel(
            old_name='Department',
            new_name='Departments',
        ),
        migrations.AlterUniqueTogether(
            name='departments',
            unique_together=set(),
        ),
        migrations.AlterModelTable(
            name='companies',
            table='companies',
        ),
        migrations.AlterModelTable(
            name='departments',
            table='departments',
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
    ]
