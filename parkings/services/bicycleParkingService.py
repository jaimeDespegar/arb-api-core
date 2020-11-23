from ..models import BicycleParking,Place,BicycleAndPlaces

class BicycleParkingService:

    def getCountFreePlaces():
        parkings = BicycleParking.objects.all()
        response = []
        for p in parkings:
            places = Place.objects.filter(bicycleParking=p)
            freePlaces = 0
            for place in places:
                if not place.occupied:
                    freePlaces = freePlaces + 1
            
            bicycleAndPlace = {
                "description": p.description,
                "number": p.number,
                "freePlaces": freePlaces
            }
            response.append(bicycleAndPlace)
        return response

    def getAllBicycleParkingAndPlaces():
        parkings = BicycleParking.objects.all()
        response = []
        for p in parkings:
            places = Place.objects.filter(bicycleParking=p)
            placesAux = []
            for place in places:
                aux = {
                        "placeNumer": place.placeNumber,
                        "occupied": place.occupied
                      }
                placesAux.append(aux)  
            
            bicycleAndPlace = {
                "description": p.description,
                "number": p.number,
                "places": placesAux
            }
            response.append(bicycleAndPlace)

        return response