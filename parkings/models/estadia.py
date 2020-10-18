from django.db import models
from .place import Place
from django.utils import timezone


class Estadia(models.Model):
    placeUsed = models.IntegerField()#models.ForeignKey(Place, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Estadia: Lugar utilizado ' + str(self.placeUsed)