from django.db import models

class BicycleParking(models.Model):
    description = models.CharField(max_length=200)
    number = models.IntegerField(default= 0)

    def __str__(self):
        return self.description