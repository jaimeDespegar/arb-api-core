from django.db import models
from django.utils import timezone
from .estadia import Estadia

class Segment(models.Model):
    typeSegment = models.CharField(max_length=8, default=None) # llegada y salida
    photoPath = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)
    estadia = models.ForeignKey(Estadia, on_delete=models.CASCADE, default=None)
    

    def __str__(self):
        return 'Segment: tipo '+self.typeSegment+', foto '+self.photoPath +' , datetime  '+ self.datetime.strftime("%m/%d/%Y - %H:%M:%S") 
 