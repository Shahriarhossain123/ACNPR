# Generated by Django 3.2.8 on 2021-10-16 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.CharField(max_length=20, verbose_name='Number Plate')),
                ('plate_photo', models.ImageField(default='platepic.png', upload_to='plate_pic', verbose_name='Number Plate Image')),
                ('entry_time', models.DateTimeField(verbose_name='Entry Time')),
                ('modify_time', models.DateTimeField()),
                ('data_entry_time', models.DateTimeField()),
            ],
        ),
    ]
