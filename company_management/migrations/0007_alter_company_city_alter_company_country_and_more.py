# Generated by Django 5.0.2 on 2024-03-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_management', '0006_alter_company_city_alter_company_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(max_length=100),
        ),
    ]
