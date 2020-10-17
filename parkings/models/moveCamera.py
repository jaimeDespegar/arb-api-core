from django.db import models

class MoveCamera(models.Model):
    placeNumber = models.IntegerField()
    occupied = models.BooleanField(default=False, blank=True, null=True)
    pathPhoto = models.CharField(max_length=200)
    hourGenerated = models.CharField(max_length=200)

    def __str__(self):
        return 'Move generated occupied: ' + str(self.occupied) 
        