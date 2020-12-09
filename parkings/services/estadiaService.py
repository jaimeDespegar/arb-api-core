from ..models import Estadia, Segment
from ..models import MoveCamera, Estadia, Place, NotificationEgress, BicycleParking, PendingStay
import time
import datetime
from collections import Counter
from .reportService import ReportService


class EstadiaService():

    def __init__(self):
        self.reportService = ReportService()

    def findAll(self):
        items = Estadia.objects.all()
        return self.parseEstadias(items)
        
    def findByFilters(self, filters, isSuspected):
        estadias = Estadia.objects.filter(**filters)
        staysFiltered = []
        if (isSuspected):
            for e in estadias:
                itemOk = len(NotificationEgress.objects.filter(estadia=e)) > 0
                if (itemOk):
                    staysFiltered.append(e)
        else:
            staysFiltered = estadias                       
        return self.parseEstadias(staysFiltered)


    def findSuspect(self):
        items = NotificationEgress.objects.all()
        estadias = Estadia.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          isAnonymous=True)
        return estadias


    def createAnonymousStay(self, arrivalMove):
        place= Place.objects.filter(placeNumber= arrivalMove.placeNumber)[0]
        anonimo = Estadia.objects.create(placeUsed=arrivalMove.placeNumber, 
                                         userName='Anonimo',
                                         isAnonymous=True,
                                         place=place)
        
        Segment.objects.create(segmentType='LLEGADA', 
                               photoPath=arrivalMove.pathPhoto, 
                               photoInBase64=arrivalMove.photoInBase64,
                               estadia=anonimo)
        
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
        place.occupied= True
        place.save()
        print('Estadia anonima creada')
    
    #solo el sgmento de salida (la estadia ya está creada)
    def createAnonymousStayOUT(self, departureMove, estadia):
        Segment.objects.create(segmentType='SALIDA', 
                               photoPath=departureMove.pathPhoto, 
                               photoInBase64=departureMove.photoInBase64,
                               estadia=estadia)
        
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
        place= estadia.place #Place.objects.filter(placeNumber= estadia.place)[0] CHEQUEAR!
        place.occupied= False
        place.save()

        estadia.isActive = False
        estadia.save()
        print('Estadia anonima cerrada')

    
    def updateAnonymousCase(self):
        exitMoves = MoveCamera.objects.filter(occupied=False, registered=False)
        
        for move in exitMoves:
            estadia = Estadia.objects.get(placeUsed=move.placeNumber, userName='Anonimo')
    
    def registerEntrance(self, data):
        
        parking = BicycleParking.objects.get(number=data['parkingNumber'])
        place = Place.objects.get(placeNumber=data['place'], bicycleParking=parking)
        try:
            stayCreated = Estadia.objects.get(place=place, isActive=True)
        except Estadia.DoesNotExist:
            stayCreated = None
        
        if (stayCreated is not None and stayCreated.isAnonymous):
            stayCreated.userName = data['userName']
            stayCreated.isAnonymous = False
            stayCreated.save()
            place = stayCreated.place
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
            place = stayCreated.place
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
                        'dateCreated': segment.dateCreated,
                        'photo': segment.photoPath,
                        'imageBase64': segment.photoInBase64
                    }
                else:
                    departure = {
                        'dateCreated': segment.dateCreated,
                        'photo': segment.photoPath,
                        'imageBase64': segment.photoInBase64
                    }

            item = {
                'id': est.id,
                'userName': est.userName, 
                'arrival': arrival, 
                'departure': departure,
                'placeUsed': est.placeUsed,
                'dateCreated': est.dateCreated,
                'isAnonymous': est.isAnonymous
            }
            
            responses.append(item)
    
        return responses

    def findSuspectEgress(self):       
        estadiaSuspected = NotificationEgress.objects.filter(isSuspected=True)
        return estadiaSuspected

    def findSuspectEgressInOneStadia(self, estadiaAnalizar):
        estadiaSuspected = NotificationEgress.objects.filter(isSuspected=True)
        return estadiaSuspected
    
    def buildReportStatistics(self):
        return self.reportService.buildReportStatistics(self.findAll(), self.findSuspectEgress())

    def generateWeekReport(self, pk_days):
        return self.reportService.generateWeekReport(pk_days)

    def generateAllEstadiaReport(self, pk):
        return self.reportService.generateAllEstadiaReport(pk)

    #Se asume que un usuario puede tener solo 1 estadía por día
    def findUserEstadiaReport(self, pk, pk_days):
        return self.reportService.findUserEstadiaReport(pk, pk_days)

    #Se asume que por cada dia hay muchos ingresos y egresos
    def findAllEstadiaReport(self, pk_days):
        return self.reportService.findAllEstadiaReport(pk_days)

    #Se asume que un usuario puede tener solo 1 estadía por día
    def findPromedioHourEstadiaReport(self):
        return self.reportService.findPromedioHourEstadiaReport()

    #Se asume que por cada dia hay muchos ingresos y egresos
    def findAllEstadiaSuspectedAndPeakTimeReport(self, pk_days):
        return self.reportService.findAllEstadiaSuspectedAndPeakTimeReport(pk_days)

    def getStatusStay(self, userName):
        try:
            pending = PendingStay.objects.get(userName=userName, isActive=True)
            status = 'PENDING'
            return {
                    'status': status, 
                    'parking': pending.stay.place.bicycleParking.description, 
                    'place': pending.stay.place.placeNumber
                   }
        except PendingStay.DoesNotExist:
            try:
                stay = Estadia.objects.filter(userName=userName, isActive=True)
                status = 'ENTRANCE_DONE' if len(stay) > 0 else 'WITH_OUT_STAY'
            except Estadia.DoesNotExist:
                status = 'WITH_OUT_STAY'
        
        return {'status': status}

    def desactiveOldEstadias(self):
        now = datetime.datetime.utcnow()
        totales = Estadia.objects.filter(isActive=True)
        for estadia in totales:
            if(estadia.dateCreated.strftime("%x")!= now.strftime("%x")):
                estadia.isActive=False
                estadia.save()