from ..models import NotificationEgress


class NotificationEgressDao:
    
    def filter(self, filters):
        return NotificationEgress.objects.filter(**filters)
    
    def getAll(self):
        return NotificationEgress.objects.all()
    
    def insert(self, newNotification):
        NotificationEgress.objects.insert(**newNotification)
        
    def get(self, filters):
        try:
            task = NotificationEgress.objects.get(**filters)
        except NotificationEgress.DoesNotExist:
            task = None