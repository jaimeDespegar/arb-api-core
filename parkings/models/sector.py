from django.db import models
from .bicycleParking import BicycleParking

class Sector(models.Model):
    placeNumber = models.IntegerField()
    bicycleParking = models.ForeignKey(BicycleParking, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.placeNumber) +' , '+ str(self.bicycleParking)