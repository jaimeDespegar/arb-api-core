from django.db import models

class Place(models.Model):
    placeNumber = models.IntegerField()
    occupied = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return 'Place number ' + str(self.placeNumber) +', is occupied ' + str(self.occupied)
        