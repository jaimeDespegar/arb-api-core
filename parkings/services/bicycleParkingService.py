from ..daos import BicycleParkingDao, PlaceDao, StayDao

class BicycleParkingService:

    def getCountFreePlaces():
        parkings = BicycleParkingDao().getAll()
        response = []
        for p in parkings:
            filters = {
                'bicycleParking__exact': p
            }
            places = PlaceDao().findByFilters(filters)
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
            filters = {
                'bicycleParking__exact': p
            }
            places = PlaceDao().findByFilters(filters)
            
            placesAux = []
            for place in places:
                
                if (place.occupied):
                    filtersStay = {
                        "place__exact": place,
                        "isActive__exact": True 
                    }
                    stay = StayDao().getByFilters(filtersStay)
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