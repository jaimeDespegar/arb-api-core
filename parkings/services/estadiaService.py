from ..models import Estadia, Segment
from ..responses import EstadiaResponse, SegmentResponse
from ..models import MoveCamera, Estadia, Place, NotificationEgress
import time


class EstadiaService():

    def findAll(self):
        items = Estadia.objects.all()
        return self.parseEstadias(items)
        
    
    def findByFilters(self, filters):
        estadias = Estadia.objects.filter(**filters)
        return self.parseEstadias(estadias)


    def findSuspect(self):
        
        items = NotificationEgress.objects.all()
        
        estadias = Estadia.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          isAnonymous=True)
        return estadias


    def createAnonymousStay(self, arrivalMove):
        anonimo = Estadia.objects.create(placeUsed=arrivalMove.placeNumber, 
                                         userName='Anonimo',
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
            estadia = Estadia.objects.get(placeUsed=move.placeNumber, userName='Anonimo')
    
    def registerEntrance(self, data):
        
        try: 
            stayCreated = Estadia.objects.get(placeUsed=data['place'], isActive=True)
        except Estadia.DoesNotExist:
            stayCreated = None
        
        if (stayCreated is not None and stayCreated.isAnonymous):
            stayCreated.userName = data['userName']
            stayCreated.isAnonymous = False
            stayCreated.save()
            place = Place.objects.filter(placeNumber= stayCreated.placeUsed)[0]
            place.occupied= True
            place.save()
            print('Estadia registrada para el usuario ' + data['userName'])
            return True;
        else:
            print('La estadia no existe o ya fue registrada por otro usuario')
            return False;


    def registerEgress(self, data):
        try: 
            stayCreated = Estadia.objects.get(userName=data['userName'], isActive=True)
        except Estadia.DoesNotExist:
            stayCreated = None
        
        if (stayCreated is not None):
            stayCreated.isActive = False
            stayCreated.save()
            place = Place.objects.filter(placeNumber= stayCreated.placeUsed)[0]
            place.occupied= False
            place.save()
            print('Estadia terminada, usuario ' + data['userName'])
            return True;
        else:
            print('No hay una estadia activa para el usuario ' + data['userName'])
            return False;


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
                'id': est.id,
                'userName': est.userName, 
                'arrival': arrival, 
                'departure': departure,
                'placeUsed': est.placeUsed,
                'dateCreated': est.dateCreated,
                'isAnonymous': est.isAnonymous
            }
            
            responses.append(e)
    
        return responses

    def findSuspectEgress(self):
        #items = NotificationEgress.objects.all()
        
        estadiaSuspected = NotificationEgress.objects.filter(isSuspected=True)
        return estadiaSuspected

    def findSuspectEgressInOneStadia(self, estadiaAnalizar):
        #items = NotificationEgress.objects.all()
        print("")
        print("findSuspectEgressInOneStadia  --inicio--")
        print(estadiaAnalizar)
        print("findSuspectEgressInOneStadia  --fin--")
        #stayCreated = Estadia.objects.get(userName="admin")
        estadiaSuspected = NotificationEgress.objects.filter(isSuspected=True)#,estadia=estadiaAnalizar
        
        return estadiaSuspected