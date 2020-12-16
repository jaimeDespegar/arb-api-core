from ..models import PendingStay


class PendingStayDao:
    
    def get(self, filters):
        try:
            return PendingStay.objects.get(**filters)
        except PendingStay.DoesNotExist:
            return None
    
    def filter(self, filters):
        return PendingStay.objects.filter(**filters)
    
    def getAll(self):
        return PendingStay.objects.all()

    def insert(self, newPending):
        PendingStay.objects.create(**newPending)