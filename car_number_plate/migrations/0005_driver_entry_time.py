# Generated by Django 3.2.8 on 2021-10-22 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_number_plate', '0004_auto_20211022_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='entry_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Entry Time'),
        ),
    ]
