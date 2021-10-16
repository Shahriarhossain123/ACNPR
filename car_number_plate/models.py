from django.db import models


# Create your models here.
class Car(models.Model):
    number_plate = models.CharField("Number Plate", max_length=20)
    plate_photo = models.ImageField("Number Plate Image", default='platepic.png', upload_to='plate_pic')
    entry_time = models.DateTimeField("Entry Time")
    modify_time = models.DateTimeField()
    data_entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number_plate
