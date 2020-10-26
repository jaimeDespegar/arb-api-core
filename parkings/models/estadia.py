from django.db import models
from .place import Place
from django.utils import timezone


class Estadia(models.Model):
    placeUsed = models.IntegerField()#models.ForeignKey(Place, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)
    userEmail = models.CharField(max_length=50, default=None)
    isAnonymous = models.BooleanField(default=False)

    def __str__(self):
        return 'Estadia: Lugar  ' + str(self.placeUsed)