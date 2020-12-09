from django.db import models
from .place import Place
from django.utils import timezone


class Estadia(models.Model):
    placeUsed = models.IntegerField()#models.ForeignKey(Place, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)
    userName = models.CharField(max_length=50, default=None)
    isAnonymous = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, default=None, null=True)


    def __str__(self):
    	return 'Estadia: user '+ self.userName + ', lugar  ' + str(self.placeUsed) + ', activa ' + str(self.isActive) + ', dateCreated ' + str(self.dateCreated)
