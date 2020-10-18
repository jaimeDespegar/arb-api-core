from django.db import models
from .place import Place

class Estadia(models.Model):
    placeUsed = models.IntegerField()#models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return 'Estadia: Lugar utilizado ' + str(self.placeUsed)