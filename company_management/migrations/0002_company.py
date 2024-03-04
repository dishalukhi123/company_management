# Generated by Django 5.0.2 on 2024-03-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('about', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('private company', 'Private Company'), ('associate aompany', 'Associate company'), ('government', 'Government')], max_length=40)),
                ('industry', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'company',
            },
        ),
    ]
