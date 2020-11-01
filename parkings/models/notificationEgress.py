from django.db import models
from .estadia import Estadia

class NotificationEgress(models.Model):
    userName = models.CharField(max_length=200)
    photoPath = models.CharField(max_length=200)
    place = models.IntegerField(default=None)
    isOk = models.BooleanField(default=True, blank=True, null=True)
    isSuspected = models.BooleanField(default=False, blank=True, null=True)
    estadia = models.ForeignKey(Estadia, on_delete=models.CASCADE)

    def __str__(self):
        return self.userName +' , '+ self.photoPath