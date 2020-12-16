from django.db import models
from .estadia import Estadia
from django.utils import timezone


class NotificationEgress(models.Model):
    userName = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True, blank=True, null=True)
    isSuspected = models.BooleanField(default=None, blank=True, null=True)
    estadia = models.ForeignKey(Estadia, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)
    photoInBase64 = models.TextField(default="", null =False)
    

    def __str__(self):
        return 'Alerta de egreso para el usuario ' + self.userName + ', isActive ' + str(self.isActive) 