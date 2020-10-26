from ..models import Estadia, Segment
from ...api.responses.estadiaResponse import EstadiaResponse, SegmentResponse
from ..models import MoveCamera, Estadia
import time

class EstadiaService():

    def findByUser(self, userName):
        # TODO
        return []


    def findByRangeDate(self, fromDate, toDate):
        responses = []
        estadias = Estadia.objects.filter(dateCreated__lte=toDate, dateCreated__gte=fromDate)

        for est in estadias:
            segments = Segment.objects.filter(estadia=est)
            for segment in segments: 
                arrival = None
                departure = None
                if segment.segmentType == 'LLEGADA':
                    arrival = SegmentResponse(segment.datetime, segment.photoPath)
                else:
                    departure = SegmentResponse(segment.datetime, segment.photoPath) 

            e = EstadiaResponse('Test', arrival, departure, est.placeUsed)
            responses.append(e)
        
        return responses


    def findAnonymous(self):
        # TODO
        return []


    def createAnonymousCase(self):
        tolerancia = 5
        arrivalMoves= MoveCamera.objects.filter(occupied=True, registered=False)

        for move in arrivalMoves:
            now = time.time()
            difference = int(now - move.createDate)

            if(difference >= tolerancia):
                anonimo = Estadia.objects.create(placeUsed=move.placeNumber, 
                                                 userEmail='Anonimo',
                                                 isAnonymous=True)
                
                Segment.objects.create(typeSegment='LLEGADA', 
                                       photoPath=move.pathPhoto, 
                                       estadia=anonimo)
                #move.registered = True
                #move.save()
                print('crear estadia anonima')
            else:
                print('no paso el tiempo de tolerancia')
    
    
    def updateAnonymousCase(self):
        exitMoves = MoveCamera.objects.filter(occupied=False, registered=False)
        
        for move in exitMoves:
            estadia = Estadia.objects.get(placeUsed=move.placeNumber, userEmail='Anonimo')