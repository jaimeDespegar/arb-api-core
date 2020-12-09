from ..models import Place


class PlaceDao:
    
    def findByFilters(self, filters):
        return Place.objects.filter(**filters)