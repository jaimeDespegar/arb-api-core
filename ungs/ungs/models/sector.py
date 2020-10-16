from django.db import models

class Sector(models.Model):
    placeNumber = models.IntegerField()
    bicycleParking = models.IntegerField()

    def __str__(self):
        return str(self.placeNumber) +' , '+ str(self.bicycleParking)