from django.db import models


# Create your models here.
class Car(models.Model):
    number_plate = models.CharField("Number Plate", max_length=20)
    plate_photo = models.ImageField("Number Plate Image", default='platepic.png', upload_to='plate_pic', blank=True,
                                    null=True)
    entry_time = models.DateTimeField("Entry Time")
    modify_time = models.DateTimeField()
    data_entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number_plate


class Driver(models.Model):
    name = models.CharField("Driver Name", max_length=300)
    phone = models.CharField("Phone", max_length=300, null=True)
    address = models.CharField("Address", max_length=300, null=True)
    car = models.ForeignKey(Car, on_delete=models.RESTRICT)
    photo = models.ImageField("Driver Photo", default='driverpic.png', upload_to='driver_pic', blank=True, null=True)
    entry_time = models.DateTimeField("Entry Time", blank=True, null=True)
    modify_time = models.DateTimeField()
    data_entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
