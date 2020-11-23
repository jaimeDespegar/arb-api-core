from ..models import Estadia, Segment
from ..models import MoveCamera, Estadia, Place, NotificationEgress
import time
import datetime
from collections import Counter

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
        print(reportStatistics)
        return reportStatistics

########################################################################

    #Se asume que un usuario puede tener solo 1 estadía por día
    def findUserEstadiaReport(self, pk, pk_days):
        print("pk: ",pk)
        print("pk_days: ",pk_days)
        #pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)


        listDaysWeek = ["LU","MA","MI","JU","VI","SA"]
        #general
        listEntrance = []
        listEgress = []
        #particular
        listEntranceLunes = []
        listEntranceMartes = []
        listEntranceMiercoles = []
        listEntranceJueves = []
        listEntranceViernes = []
        listEntranceSabado = []
        listEgressLunes = []
        listEgressMartes = []
        listEgressMiercoles = []
        listEgressJueves = []
        listEgressViernes = []
        listEgressSabado = []

        for i in range(pk_days):
            print("\n\n\n\n")
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            estadiaUser = Estadia.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          userName= pk)
            print("estadiaUser:")
            print(estadiaUser)
            print("len(estadiaUser) :", len(estadiaUser) )
            if(len(estadiaUser) == 1):
                segmentUser = Segment.objects.filter(segmentType= "SALIDA",
                                          estadia= estadiaUser[0])[0]
                print(segmentUser)
                if(segmentUser is not None):
                    horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
                    horaEgreso= int(segmentUser.dateCreated.strftime("%H"))

                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Monday"): 
                        listEntranceLunes.append(horaIngreso)
                        listEgressLunes.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Tuesday"): 
                        listEntranceMartes.append(horaIngreso)
                        listEgressMartes.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Wednesday"): 
                        listEntranceMiercoles.append(horaIngreso)
                        listEgressMiercoles.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Thursday"): 
                        listEntranceJueves.append(horaIngreso)
                        listEgressJueves.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Friday"): 
                        listEntranceViernes.append(horaIngreso)
                        listEgressViernes.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Saturday"): 
                        listEntranceSabado.append(horaIngreso)
                        listEgressSabado.append(horaEgreso)
        
        #Validación de listas NO vacías
        if(len(listEntranceLunes)==0):
            listEntranceLunes.append(0)
        if(len(listEntranceMartes)==0):
            listEntranceMartes.append(0)
        if(len(listEntranceMiercoles)==0):
            listEntranceMiercoles.append(0)
        if(len(listEntranceJueves)==0):
            listEntranceJueves.append(0)
        if(len(listEntranceViernes)==0):
            listEntranceViernes.append(0)
        if(len(listEntranceSabado)==0):
            listEntranceSabado.append(0)

        if(len(listEgressLunes)==0):
            listEgressLunes.append(0)
        if(len(listEgressMartes)==0):
            listEgressMartes.append(0)
        if(len(listEgressMiercoles)==0):
            listEgressMiercoles.append(0)
        if(len(listEgressJueves)==0):
            listEgressJueves.append(0)
        if(len(listEgressViernes)==0):
            listEgressViernes.append(0)
        if(len(listEgressSabado)==0):
            listEgressSabado.append(0)

        #ingresos por dias
        Ilu = Counter(listEntranceLunes)
        Ima = Counter(listEntranceMartes)
        Imi = Counter(listEntranceMiercoles)
        Iju = Counter(listEntranceJueves)
        Ivi = Counter(listEntranceViernes)
        Isa = Counter(listEntranceSabado)
        #lista final de ingresos
        listEntrance.append("Ingresos: ")
        listEntrance.append(max(Ilu, key=Ilu.get))
        listEntrance.append(max(Ima, key=Ima.get))
        listEntrance.append(max(Imi, key=Imi.get))
        listEntrance.append(max(Iju, key=Iju.get))
        listEntrance.append(max(Ivi, key=Ivi.get))
        listEntrance.append(max(Isa, key=Isa.get))

        #egresos por dias
        Olu = Counter(listEgressLunes)
        Oma = Counter(listEgressMartes)
        Omi = Counter(listEgressMiercoles)
        Oju = Counter(listEgressJueves)
        Ovi = Counter(listEgressViernes)
        Osa = Counter(listEgressSabado)
        #lista final de egresos
        listEgress.append("Egresos: ")
        listEgress.append(max(Olu, key=Olu.get))
        listEgress.append(max(Oma, key=Oma.get))
        listEgress.append(max(Omi, key=Omi.get))
        listEgress.append(max(Oju, key=Oju.get))
        listEgress.append(max(Ovi, key=Ovi.get))
        listEgress.append(max(Osa, key=Osa.get))

        reportStatistics = {
            "listDaysWeek": listDaysWeek,
            "listEntrance": listEntrance, 
            "listEgress": listEgress,
        }
        print(reportStatistics)

        reportStatistics3 = {
            "modo": "Ingresos",
            "lunes": max(Ilu, key=Ilu.get),
            "martes": max(Ima, key=Ima.get),
            "miercoles": max(Imi, key=Imi.get),
            "jueves": max(Iju, key=Iju.get),
            "viernes": max(Ivi, key=Ivi.get),
            "sabado": max(Isa, key=Isa.get),
        }
        reportStatistics4 = {
            "modo": "Egresos",
            "lunes": max(Olu, key=Olu.get),
            "martes": max(Oma, key=Oma.get),
            "miercoles": max(Omi, key=Omi.get),
            "jueves": max(Oju, key=Oju.get),
            "viernes": max(Ovi, key=Ovi.get),
            "sabado": max(Osa, key=Osa.get),
        }

        lista = []
        lista.append(reportStatistics3)
        lista.append(reportStatistics4)
        return lista

########################################################################

    #Se asume que por cada dia hay muchos ingresos y egresos
    def findAllEstadiaReport(self, pk_days):
        pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)


        listDaysWeek = ["LU","MA","MI","JU","VI","SA"]
        #general
        listEntrance = []
        listEgress = []
        #particular
        listEntranceLunes = []
        listEntranceMartes = []
        listEntranceMiercoles = []
        listEntranceJueves = []
        listEntranceViernes = []
        listEntranceSabado = []
        listEgressLunes = []
        listEgressMartes = []
        listEgressMiercoles = []
        listEgressJueves = []
        listEgressViernes = []
        listEgressSabado = []

        for i in range(pk_days):
            print("\n\n\n\n")
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales= Segment.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          segmentType= "SALIDA")
            for segmentUser in totales:
                horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
                horaEgreso= int(segmentUser.dateCreated.strftime("%H"))

                if(segmentUser.estadia.dateCreated.strftime("%A")=="Monday"): 
                    listEntranceLunes.append(horaIngreso)
                    listEgressLunes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Tuesday"): 
                    listEntranceMartes.append(horaIngreso)
                    listEgressMartes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Wednesday"): 
                    listEntranceMiercoles.append(horaIngreso)
                    listEgressMiercoles.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Thursday"): 
                    listEntranceJueves.append(horaIngreso)
                    listEgressJueves.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Friday"): 
                    listEntranceViernes.append(horaIngreso)
                    listEgressViernes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Saturday"): 
                    listEntranceSabado.append(horaIngreso)
                    listEgressSabado.append(horaEgreso)

        #Validación de listas NO vacías
        if(len(listEntranceLunes)==0):
            listEntranceLunes.append(0)
        if(len(listEntranceMartes)==0):
            listEntranceMartes.append(0)
        if(len(listEntranceMiercoles)==0):
            listEntranceMiercoles.append(0)
        if(len(listEntranceJueves)==0):
            listEntranceJueves.append(0)
        if(len(listEntranceViernes)==0):
            listEntranceViernes.append(0)
        if(len(listEntranceSabado)==0):
            listEntranceSabado.append(0)

        if(len(listEgressLunes)==0):
            listEgressLunes.append(0)
        if(len(listEgressMartes)==0):
            listEgressMartes.append(0)
        if(len(listEgressMiercoles)==0):
            listEgressMiercoles.append(0)
        if(len(listEgressJueves)==0):
            listEgressJueves.append(0)
        if(len(listEgressViernes)==0):
            listEgressViernes.append(0)
        if(len(listEgressSabado)==0):
            listEgressSabado.append(0)

        #ingresos por dias
        Ilu = Counter(listEntranceLunes)
        Ima = Counter(listEntranceMartes)
        Imi = Counter(listEntranceMiercoles)
        Iju = Counter(listEntranceJueves)
        Ivi = Counter(listEntranceViernes)
        Isa = Counter(listEntranceSabado)
        #lista final de ingresos
        listEntrance.append(max(Ilu, key=Ilu.get))
        listEntrance.append(max(Ima, key=Ima.get))
        listEntrance.append(max(Imi, key=Imi.get))
        listEntrance.append(max(Iju, key=Iju.get))
        listEntrance.append(max(Ivi, key=Ivi.get))
        listEntrance.append(max(Isa, key=Isa.get))

        #egresos por dias
        Olu = Counter(listEgressLunes)
        Oma = Counter(listEgressMartes)
        Omi = Counter(listEgressMiercoles)
        Oju = Counter(listEgressJueves)
        Ovi = Counter(listEgressViernes)
        Osa = Counter(listEgressSabado)
        #lista final de egresos
        listEgress.append(max(Olu, key=Olu.get))
        listEgress.append(max(Oma, key=Oma.get))
        listEgress.append(max(Omi, key=Omi.get))
        listEgress.append(max(Oju, key=Oju.get))
        listEgress.append(max(Ovi, key=Ovi.get))
        listEgress.append(max(Osa, key=Osa.get))

        listEntranceFinal = []
        listEntranceFinal.append(listEntrance)
        listEgressFinal = []
        listEgressFinal.append(listEgress)
        reportStatistics = {
            "listDaysWeek": listDaysWeek,
            "listEntrance": listEntranceFinal, 
            "listEgress": listEgressFinal,
        }
        print(reportStatistics)
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

########################################################################


########################################################################

    #Se asume que por cada dia hay muchos ingresos y egresos
    def findAllEstadiaSuspectedAndPeakTimeReport(self, pk_days):
        pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)


        listDaysWeek = ["LU","MA","MI","JU","VI","SA"]
        #general
        listHoursParking = []
        listEgressSuspected = []
        #particular
        listHoursParkingLunes = []
        listHoursParkingMartes = []
        listHoursParkingMiercoles = []
        listHoursParkingJueves = []
        listHoursParkingViernes = []
        listHoursParkingSabado = []

        listEgressSuspectedLunes = []
        listEgressSuspectedMartes = []
        listEgressSuspectedMiercoles = []
        listEgressSuspectedJueves = []
        listEgressSuspectedViernes = []
        listEgressSuspectedSabado = []

        for i in range(pk_days):
            print("\n\n\n\n")
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales= Segment.objects.filter(dateCreated__lte=toDate, 
                                          dateCreated__gte=fromDate,
                                          segmentType= "LLEGADA")

            for segmentUser in totales:
                horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
                horaEgreso= int(segmentUser.dateCreated.strftime("%H"))
                listaRangoDeUso= list(range(horaIngreso,horaEgreso+1))
                sospechosa = NotificationEgress.objects.filter(isSuspected=True,
                                                    estadia=segmentUser.estadia)

                if(segmentUser.estadia.dateCreated.strftime("%A")=="Monday"): 
                    listHoursParkingLunes=listHoursParkingLunes+listaRangoDeUso
                    if(sospechosa is not None):
                        listEgressSuspectedLunes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Tuesday"): 
                    listHoursParkingMartes= listHoursParkingMartes+listaRangoDeUso
                    if(sospechosa is not None):
                        listEgressSuspectedMartes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Wednesday"): 
                    listHoursParkingMiercoles= listHoursParkingMiercoles+listaRangoDeUso
                    if(sospechosa is not None):
                        listEgressSuspectedMiercoles.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Thursday"): 
                    listHoursParkingJueves= listHoursParkingJueves+listaRangoDeUso
                    if(sospechosa is not None):
                        listEgressSuspectedJueves.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Friday"): 
                    listHoursParkingViernes= listHoursParkingViernes+listaRangoDeUso
                    if(sospechosa is not None):
                        listEgressSuspectedViernes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Saturday"): 
                    listHoursParkingSabado= listHoursParkingSabado+listaRangoDeUso
                    if(sospechosa is not None):
                        listEgressSuspectedSabado.append(horaEgreso)



        #Validación de listas NO vacías
        if(len(listHoursParkingLunes)==0):
            listHoursParkingLunes.append(0)
        if(len(listHoursParkingMartes)==0):
            listHoursParkingMartes.append(0)
        if(len(listHoursParkingMiercoles)==0):
            listHoursParkingMiercoles.append(0)
        if(len(listHoursParkingJueves)==0):
            listHoursParkingJueves.append(0)
        if(len(listHoursParkingViernes)==0):
            listHoursParkingViernes.append(0)
        if(len(listHoursParkingSabado)==0):
            listHoursParkingSabado.append(0)

        if(len(listEgressSuspectedLunes)==0):
            listEgressSuspectedLunes.append(0)
        if(len(listEgressSuspectedMartes)==0):
            listEgressSuspectedMartes.append(0)
        if(len(listEgressSuspectedMiercoles)==0):
            listEgressSuspectedMiercoles.append(0)
        if(len(listEgressSuspectedJueves)==0):
            listEgressSuspectedJueves.append(0)
        if(len(listEgressSuspectedViernes)==0):
            listEgressSuspectedViernes.append(0)
        if(len(listEgressSuspectedSabado)==0):
            listEgressSuspectedSabado.append(0)

        #ingresos por dias
        Ilu = Counter(listHoursParkingLunes)
        Ima = Counter(listHoursParkingMartes)
        Imi = Counter(listHoursParkingMiercoles)
        Iju = Counter(listHoursParkingJueves)
        Ivi = Counter(listHoursParkingViernes)
        Isa = Counter(listHoursParkingSabado)
        #lista final de ingresos
        listHoursParking.append(max(Ilu, key=Ilu.get))
        listHoursParking.append(max(Ima, key=Ima.get))
        listHoursParking.append(max(Imi, key=Imi.get))
        listHoursParking.append(max(Iju, key=Iju.get))
        listHoursParking.append(max(Ivi, key=Ivi.get))
        listHoursParking.append(max(Isa, key=Isa.get))

        #egresos por dias
        Olu = Counter(listEgressSuspectedLunes)
        Oma = Counter(listEgressSuspectedMartes)
        Omi = Counter(listEgressSuspectedMiercoles)
        Oju = Counter(listEgressSuspectedJueves)
        Ovi = Counter(listEgressSuspectedViernes)
        Osa = Counter(listEgressSuspectedSabado)
        #lista final de egresos
        listEgressSuspected.append(max(Olu, key=Olu.get))
        listEgressSuspected.append(max(Oma, key=Oma.get))
        listEgressSuspected.append(max(Omi, key=Omi.get))
        listEgressSuspected.append(max(Oju, key=Oju.get))
        listEgressSuspected.append(max(Ovi, key=Ovi.get))
        listEgressSuspected.append(max(Osa, key=Osa.get))

        listHoursParkingFinal = []
        listHoursParkingFinal.append(listHoursParking)
        listEgressSuspectedFinal = []
        listEgressSuspectedFinal.append(listEgressSuspected)
        reportStatistics = {
            "listDaysWeek": listDaysWeek,
            "listHoursParkingFinal": listHoursParkingFinal, 
            "listEgressSuspectedFinal": listEgressSuspectedFinal,
        }
        print(reportStatistics)
        return reportStatistics
