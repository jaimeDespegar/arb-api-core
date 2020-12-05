from django.db import models

class Configuration(models.Model):
    
    configurationName = models.CharField(max_length=200, default='config', null=True)
    configurationValue = models.IntegerField(default=1)
    
    def __str__(self):
        return 'Configuracion: ' + self.configurationName + ' - ' + str(self.configurationValue)