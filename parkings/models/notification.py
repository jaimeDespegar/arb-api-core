from django.db import models

class Notification(models.Model):
    userName = models.CharField(max_length=200)
    photoPath = models.CharField(max_length=200)
    place = models.IntegerField(default=None)

    def __str__(self):
        return self.userName +' , '+ self.photoPath
        