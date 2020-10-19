from ..models import BicycleParking,Place

class BicycleParkingService:

    def getCountFreePlaces():
        parkings = BicycleParking.objects.all()
        freePlaces = 0
        for p in parkings:
            places = Place.objects.filter(bicycleParking=p)
            for place in places:
                if not place.occupied:
                    freePlaces = freePlaces + 1
        
        return freePlaces