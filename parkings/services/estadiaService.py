from ..models import Estadia, Segment
from ..responses import EstadiaResponse, SegmentResponse
from ..models import MoveCamera, Estadia, Place
import time


class EstadiaService():

    def findAll(self):
        items = Estadia.objects.all()
        return self.parseEstadias(items)
    
    
    def findByUser(self, userName):
        estadias = Estadia.objects.filter(userName=userName)
        return estadias


    def findByRangeDate(self, fromDate, toDate):
        estadias = Estadia.objects.filter(dateCreated__lte=toDate, dateCreated__gte=fromDate)
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
        
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
        place= Place.objects.filter(placeNumber= anonimo.placeUsed)[0]
        place.occupied= True
        place.save()
        print('Estadia anonima creada')
    
    #solo el sgmento de salida (la estadia ya está creada)
    def createAnonymousStayOUT(self, arrivalMove, estadia):
        Segment.objects.create(segmentType='SALIDA', 
                               photoPath=arrivalMove.pathPhoto, 
                               estadia=estadia)
        
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
        place= Place.objects.filter(placeNumber= estadia.placeUsed)[0]
        place.occupied= False
        place.save()
        print('Estadia anonima cerrada')

    
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