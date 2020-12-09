from django.db import models

class MoveCamera(models.Model):
    placeNumber = models.IntegerField()
    occupied = models.BooleanField(default=False, blank=True, null=True)
    pathPhoto = models.CharField(max_length=200)
    createDate = models.CharField(default=None, max_length=200)
    registered = models.BooleanField(default=False, blank=True, null=True)
    photoInBase64 = models.TextField(default="", null =False)
    
    def __str__(self):
        return 'Move generated occupied: ' + str(self.occupied) +' in position '+str(self.placeNumber)
        