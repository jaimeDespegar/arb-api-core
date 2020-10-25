
from ..models import MoveCamera

class Validator:

    def isValidSegment(self, estadia, typeSegment):
        placeNumber=estadia['placeUsed']
        occupied = typeSegment == "LLEGADA"
        try:
           move = MoveCamera.objects.get(placeNumber=placeNumber, 
                                         occupied=occupied, 
                                         registered=False)
        except MoveCamera.DoesNotExist:
           move = None

        if (move is not None): # and (move.occupied) and (not move.registered)
            move.registered=True
            move.save()
            return True # match!
        else:
            print("No es posible efectuar la estadia")
            return False
    
    def validateLocation(self, x, y):
        print('mi point is : ' + str(x)+ ' , '+ str(y))
        parkings = BicycleParking.objects.all()
        # ver como validar la ubicacion que me envian contra la position del bicicletero
        for p in parkings:
            print(p)
        return True#Response({'isOkLocation': True}, status=status.HTTP_201_CREATED)