from django.db import models

class Estadia(models.Model):
    arrival = models.IntegerField()
    departure = models.IntegerField()
    sectorUsed = models.IntegerField()

    def __str__(self):
        return 'Llegada '+self.arrival+' Salida '+self.departure+' del sector '+self.sectorUsed