from django.db import models
from .estadia import Estadia
from django.utils import timezone


class PendingStay(models.Model):
    userName = models.CharField(max_length=50, default=None)
    isAuthorize = models.BooleanField(default=None, null=True, blank=True)
    dateCreated = models.DateTimeField(default=timezone.now)
    isActive = models.BooleanField(default=True)
    notifyToUser = models.BooleanField(default=False)
    stay = models.ForeignKey(Estadia, on_delete=models.CASCADE)

    def __str__(self):
        return 'Estadia Pendiente: la reclama '+ self.userName + ' isAuthorize ' + str(self.isAuthorize)