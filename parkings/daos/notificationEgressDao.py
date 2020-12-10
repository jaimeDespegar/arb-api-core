from ..models import NotificationEgress


class NotificationEgressDao:
    
    def filter(self, filters):
        return NotificationEgress.objects.filter(**filters)
    
    def getAll(self):
        return NotificationEgress.objects.all()