from ..models import Estadia, Segment
from ..models import MoveCamera, Estadia, Place, NotificationEgress, BicycleParking, PendingStay
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
        place= estadia.place #Place.objects.filter(placeNumber= estadia.place)[0] CHEQUEAR!
        place.occupied= False
        place.save()

        estadia.isActive = False
        estadia.save()
        print('Estadia anonima cerrada')

    
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
            # place = stayCreated.place
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
                        'photo': segment.photoPath
                    }
                else:
                    departure = {
                        'dateCreated': segment.dateCreated,
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

            listLastDaysWeek.append(toDate.strftime("%a %x"))
            

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

########################################################################

    def generateAllEstadiaReport(self, pk):
        #pk=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk)


        listLastDaysWeek = []
        listEntrance = []
        listEgress = []
        listEgressSuspected = []

        for i in range(pk):
            print("\n\n\n\n")
            day1= pk-i
            day2= pk-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales = Segment.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          segmentType= "SALIDA")

            cantIngresosTM=0
            cantIngresosTT=0
            cantIngresosTN=0
            cantEgresosTM=0
            cantEgresosTT=0
            cantEgresosTN=0
            cantEgresosSospechososTM=0
            cantEgresosSospechososTT=0
            cantEgresosSospechososTN=0

            for segment in totales:

                horaIngreso=int(segment.estadia.dateCreated.strftime("%H"))
                horaEgreso= int(segment.dateCreated.strftime("%H"))
                sospechosa = NotificationEgress.objects.filter(isSuspected=True,estadia=segment.estadia)

                #Ingreso
                if(horaIngreso>=7 and horaIngreso<=13):
                    cantIngresosTM= cantIngresosTM +1
                if(horaIngreso>13 and horaIngreso<=17):
                    cantIngresosTT= cantIngresosTT +1
                if(horaIngreso>17 and horaIngreso<=23):
                    cantIngresosTN= cantIngresosTN +1

                #Egreso
                if(horaEgreso>=7 and horaEgreso<=13):
                    cantEgresosTM= cantEgresosTM +1
                    if(len(sospechosa)>=1):
                        cantEgresosSospechososTM= cantEgresosSospechososTM +1
                if(horaEgreso>13 and horaEgreso<=17):
                    cantEgresosTT= cantEgresosTT +1
                    if(len(sospechosa)>=1):
                        cantEgresosSospechososTT= cantEgresosSospechososTT +1
                if(horaEgreso>17 and horaEgreso<=23):
                    cantEgresosTN= cantEgresosTN +1
                    if(len(sospechosa)>=1):
                        cantEgresosSospechososTN= cantEgresosSospechososTN +1

            listLastDaysWeek.append(toDate.strftime("%d"+str(" TM")))
            listLastDaysWeek.append(toDate.strftime("%d"+str(" TT")))
            listLastDaysWeek.append(toDate.strftime("%d"+str(" TN")))

            listEntrance.append(cantIngresosTM)
            listEntrance.append(cantIngresosTT)
            listEntrance.append(cantIngresosTN)

            listEgress.append(cantEgresosTM)
            listEgress.append(cantEgresosTT)
            listEgress.append(cantEgresosTN)

            listEgressSuspected.append(cantEgresosSospechososTM)
            listEgressSuspected.append(cantEgresosSospechososTT)
            listEgressSuspected.append(cantEgresosSospechososTN)

        reportStatistics = {
            "listLastDaysWeek": listLastDaysWeek,
            "listEntrance": listEntrance, 
            "listEgress": listEgress,
            "listEgressSuspected": listEgressSuspected,
        }
        
        return reportStatistics

########################################################################

    #Se asume que un usuario puede tener solo 1 estadía por día
    def findUserEstadiaReport(self, pk):
        pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)


        listLastDaysWeek = []
        listEntrance = []
        listEgress = []

        for i in range(pk_days):
            print("\n\n\n\n")
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            estadiaUser = Estadia.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          userName= pk)

            segmentUser = Segment.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          segmentType= "SALIDA",
                                          estadia= estadiaUser)

            horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
            horaEgreso= int(segmentUser.dateCreated.strftime("%H"))

            listLastDaysWeek.append(toDate.strftime("%d"))
            listEntrance.append(horaIngreso)
            listEgress.append(horaEgreso)

        reportStatistics = {
            "listLastDaysWeek": listLastDaysWeek,
            "listEntrance": listEntrance, 
            "listEgress": listEgress,
        }
        
        return reportStatistics

########################################################################

    #Se asume que un usuario puede tener solo 1 estadía por día
    def findPromedioHourEstadiaReport(self):
        pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)

        listLastDaysWeek = []
        listEntrance = []
        listEgress = []

        for i in range(pk_days):
            listEntranceDay = []
            listEgressDay = []
            print("\n\n\n\n")
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales = Segment.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          segmentType= "SALIDA")
            
            for segment in totales:
                horaIngreso=int(segment.estadia.dateCreated.strftime("%H"))
                listEntranceDay.append(horaIngreso)
                horaEgreso= int(segment.dateCreated.strftime("%H"))
                listEgressDay.append(horaEgreso)

            sumEntrance=0.0
            for i in range(0,len(listEntranceDay)):
                sumEntrance=sumEntrance+listEntranceDay[i]
            horaIngresoPromedio= sumEntrance/len(listEntranceDay)

            sumEgress=0.0
            for i in range(0,len(listEgressDay)):
                sumEgress=sumEgress+listEgressDay[i]
            horaEgresoPromedio= sumEgress/len(listEgressDay)

            listLastDaysWeek.append(toDate.strftime("%d"))
            listEntrance.append(horaIngresoPromedio)
            listEgress.append(horaEgresoPromedio)
        reportStatistics = {
            "listLastDaysWeek": listLastDaysWeek,
            "listEntrance": listEntrance, 
            "listEgress": listEgress,
        }
        
        return reportStatistics


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