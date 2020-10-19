from django.db import models
from .bicycleParking import BicycleParking

class BicycleAndPlaces():

    def __init__(self, description, numBicycle, listPlaces):
        self.description = description
        self.numBicycle = numBicycle
        self.listPlaces = listPlaces

    def __str__(self):
        return 'Descripcion ' + str(self.description) +', numero de bicicletero ' + str(self.numBicycle) +', lista de lugares' + str(self.listPlaces) 

    