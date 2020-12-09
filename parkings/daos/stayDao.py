from ..models import Estadia


class StayDao:
    
    def getByFilters(self, filters):
        try:
            return Estadia.objects.get(**filters)
        except Estadia.DoesNotExist:
            return None