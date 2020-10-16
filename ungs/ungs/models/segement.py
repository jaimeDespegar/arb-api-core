from django.db import models
from django.utils import timezone

class Segment(models.Model):
    photoPath = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.photoPath +', producido a las '+ self.datetime 