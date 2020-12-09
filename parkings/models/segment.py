from django.db import models
from django.utils import timezone
from .estadia import Estadia

class Segment(models.Model):
    segmentType = models.CharField(max_length=8, default=None) # llegada y salida
    photoPath = models.CharField(max_length=200)
    dateCreated = models.DateTimeField(default=timezone.now)
    estadia = models.ForeignKey(Estadia, on_delete=models.CASCADE, default=None)
    photoInBase64 = models.TextField(default="", null =False)

    def __str__(self):
        return 'Segment: tipo '+self.segmentType+', foto '+self.photoPath +' , dateCreated  '+ self.dateCreated.strftime("%m/%d/%Y - %H:%M:%S") 
 