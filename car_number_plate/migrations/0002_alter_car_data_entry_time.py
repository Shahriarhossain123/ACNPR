# Generated by Django 3.2.8 on 2021-10-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_number_plate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='data_entry_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
