from django.db import models
from django.utils import timezone
from .estadia import Estadia

class Segment(models.Model):
    photoPath = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)
    estadia = models.ForeignKey(Estadia, on_delete=models.CASCADE, default=None)
   

    def __str__(self):
        return 'Path foto: '+self.photoPath +' , producido a las:  '+ str(self.datetime) 