from django.db import models

class BicycleParking(models.Model):
    description = models.CharField(max_length=200)
    number = models.IntegerField(default= 0)
    positionX = models.DecimalField(default= None, max_digits = 40, decimal_places = 12, null=True)
    positionY = models.DecimalField(default= None, max_digits = 40, decimal_places = 12, null=True)
    # id = models.AutoField(primary_key=True)
    def __str__(self):
        return 'Nro ' + str(self.number) + ' - ' + self.description + ' , position '+str(self.positionX)+ ' - '+str(self.positionY)