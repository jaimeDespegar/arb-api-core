from ..models import BicycleParking

class BicycleParkingDao:
    
    def getAll(self):
        items = BicycleParking.objects.all()
        return items
    
    def getByFilters(self, filters):
        return BicycleParking.objects.get(**filters)
    
    def filter(self, filters):
        return BicycleParking.objects.filter(**filters)