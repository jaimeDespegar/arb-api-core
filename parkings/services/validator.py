
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
            