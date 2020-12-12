from ..models import Estadia


class StayDao:
    
    def get(self, filters):
        try:
            return Estadia.objects.get(**filters)
        except Estadia.DoesNotExist:
            return None
    
    def filter(self, filters):
        return Estadia.objects.filter(**filters)
    
    def insert(self, newStay):
        return Estadia.objects.create(**newStay)
    
    def getAll(self):
        return Estadia.objects.all()