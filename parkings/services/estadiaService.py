from ..models import Estadia, Segment
from ..responses import EstadiaResponse, SegmentResponse
from ..models import MoveCamera, Estadia
import time


class EstadiaService():

    def findAll(self):
        items = Estadia.objects.all()
        return self.parseEstadias(items)
        
    
    def findByFilters(self, filters):
        estadias = Estadia.objects.filter(**filters)
        return self.parseEstadias(estadias)


    def findAnonymous(self):
        fromDate='init date'
        toDate='final date'
        
        estadias = Estadia.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          isAnonymous=True)
        return estadias


    def createAnonymousStay(self, arrivalMove):
        anonimo = Estadia.objects.create(placeUsed=arrivalMove.placeNumber, 
                                         userEmail='Anonimo',
                                         isAnonymous=True)
        
        Segment.objects.create(segmentType='LLEGADA', 
                               photoPath=arrivalMove.pathPhoto, 
                               estadia=anonimo)
        
        print('Estadia anonima creada')
    
    
    def updateAnonymousCase(self):
        exitMoves = MoveCamera.objects.filter(occupied=False, registered=False)
        
        for move in exitMoves:
            estadia = Estadia.objects.get(placeUsed=move.placeNumber, userEmail='Anonimo')
    
            
    def parseEstadias(self, modelEstadias):
        responses = []
        
        for est in modelEstadias:
            segments = Segment.objects.filter(estadia=est)
            arrival = {}
            departure = {}
            for segment in segments:    
                if segment.segmentType == 'LLEGADA':
                    arrival = {
                        'dateCreated': segment.datetime,
                        'photo': segment.photoPath
                    }
                else:
                    departure = {
                        'dateCreated': segment.datetime,
                        'photo': segment.photoPath
                    }

            e = {
                'userName': 'Test '+str(est.placeUsed), 
                'arrival': arrival, 
                'departure': departure,
                'placeUsed': est.placeUsed,
                'dateCreated': est.dateCreated
            }
            
            responses.append(e)
    
        return responses