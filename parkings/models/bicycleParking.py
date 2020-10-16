from django.db import models

class BicycleParking(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description