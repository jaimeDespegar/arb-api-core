from ..models import BicycleParking,Place,BicycleAndPlaces

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

    #Descripcion de cada bicicletero
    def getDescriptonBicycleParking():
        parkings = BicycleParking.objects.all()
        response = []
        for p in parkings:
            places = Place.objects.filter(bicycleParking=p)
            bicycleAndPace = BicycleAndPlaces(p.description,p.number ,places)
            response.append(bicycleAndPace)

        return response