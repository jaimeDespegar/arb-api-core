from ..models import Place


class PlaceDao:
    
    def filter(self, filters):
        return Place.objects.filter(**filters)
    
    def get(self, filters):
        return Place.objects.get(**filters)