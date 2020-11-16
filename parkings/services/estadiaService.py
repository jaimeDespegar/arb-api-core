from ..models import Estadia, Segment
from ..models import MoveCamera, Estadia, Place, NotificationEgress
import time
import datetime


class EstadiaService():

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
                               estadia=anonimo)
        
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
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

        estadia.isActive = False
        estadia.save()
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
                        'dateCreated': segment.datetime,
                        'photo': segment.photoPath
                    }
                else:
                    departure = {
                        'dateCreated': segment.datetime,
                        'photo': segment.photoPath
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
        cantTotal= 0
        cantSospechosas = 0
        cantOk = 0

        totales = self.findAll()
        cantTotal = len(totales)

        sospechosas = self.findSuspectEgress()
        cantSospechosas = len(sospechosas)
        Sospechosas = int(((cantSospechosas)/cantTotal)*100)

        Ok = int(((cantTotal - cantSospechosas)/cantTotal)*100)

        reportStatistics = {
            "Sospechosas": Sospechosas, 
            "Ok": Ok 
        }
        return reportStatistics

    def generateWeekReport(self):
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=7)


        listLastDaysWeek = []
        listOk = []
        listSospechosas = []

        for i in range(7):
            print("\n\n\n\n")
            #busco desde el día más viejo
            day1= 7-i
            day2= 6-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            listLastDaysWeek.append(toDate)

            totales = Estadia.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate)
            cantTotal= 0
            cantSospechosas= 0
            cantOk= 0
            Sospechosas=0
            cantTotal = len(totales)

            for estadia in totales:
                sospechosa = NotificationEgress.objects.filter(isSuspected=True,estadia=estadia)
                #if(sospechosa != None):
                if(len(sospechosa)>=1):
                    cantSospechosas= cantSospechosas +1

            if(cantTotal==0):
                Sospechosas=0
                Ok=0
            else:
                Sospechosas=cantSospechosas
                Ok= cantTotal - cantSospechosas

            if(cantTotal != 0):
                if(cantSospechosas==0):
                    Ok=cantTotal

            listSospechosas.append(Sospechosas)
            listOk.append(Ok)

        reportStatistics = {
            "listaFechas": listLastDaysWeek,
            "listaSospechosas": listSospechosas, 
            "listaOk": listOk 
        }
        
        return reportStatistics