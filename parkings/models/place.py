from django.db import models
from .bicycleParking import BicycleParking

class Place(models.Model):
    placeNumber = models.IntegerField()
    occupied = models.BooleanField(default=False, blank=True, null=True)
    bicycleParking = models.ForeignKey(BicycleParking, on_delete=models.CASCADE)

    def __str__(self):
        return 'Place ' + str(self.placeNumber) +' - '+self.bicycleParking.description +' - is occupied ' + str(self.occupied)
        