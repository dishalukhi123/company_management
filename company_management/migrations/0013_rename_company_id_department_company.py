# Generated by Django 5.0.2 on 2024-03-06 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_management', '0012_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='company_id',
            new_name='company',
        ),
    ]
