from ..models import PendingStay


class PendingStayDao:
    
    def get(self, filters):
        try:
            return PendingStay.objects.get(**filters)
        except PendingStay.DoesNotExist:
            return None