from ..daos import BicycleParkingDao, PlaceDao, StayDao

class BicycleParkingService:

    def getCountFreePlaces():
        parkings = BicycleParkingDao().getAll()
        response = []
        for p in parkings:
            places = PlaceDao().filter({ 'bicycleParking__exact': p })
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
        parkings = BicycleParkingDao().getAll()
        response = []
        for p in parkings:
            places = PlaceDao().filter({ 'bicycleParking__exact': p })
            placesAux = []
            for place in places:
                if (place.occupied):
                    filtersStay = { "place__exact": place, "isActive__exact": True }
                    stay = StayDao().get(filtersStay)
                    if (stay is not None and stay.isAnonymous):
                        dateAssociatedStay = stay.dateCreated
                    else:
                        dateAssociatedStay = ''
                else:
                    dateAssociatedStay = ''
                
                aux = {
                        "placeNumber": place.placeNumber,
                        "occupied": place.occupied,
                        "dateAssociatedStay": dateAssociatedStay
                      }
                placesAux.append(aux)  
            
            bicycleAndPlace = {
                "description": p.description,
                "number": p.number,
                "places": placesAux
            }
            response.append(bicycleAndPlace)

        return response
    
    def getAll():
        return BicycleParkingDao().getAll()
    
    def get(self, filters):
        return BicycleParkingDao().getByFilters(filters)
    
    def filter(self, filters):
        return BicycleParkingDao().filter(filters)    
    
    def createPlace(self, place):
        PlaceDao().insert(place)
    
    def getPlace(self, filters):
        return PlaceDao().get(filters)