from ..models import Configuration

class ConfigurationDao:
    
    def get(self, filters):
        try:
            return Configuration.objects.get(**filters)
        except Configuration.DoesNotExist:
            return None