# Generated by Django 5.0.2 on 2024-03-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_management', '0005_remove_company_other_location_company_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
