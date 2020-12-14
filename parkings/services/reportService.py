import time
import datetime
from collections import Counter
from ..daos import SegmentDao, StayDao, NotificationEgressDao


class ReportService():
    
    def __init__(self):
        self.segmentDao = SegmentDao()
        self.notificationEgressDao = NotificationEgressDao()
        self.stayDao = StayDao()
    
    def buildReportStatistics(self, totalesAll, suspectEgress):
        cantTotal= 0
        cantSospechosas = 0
        cantOk = 0

        totales = totalesAll
        cantTotal = len(totales)

        sospechosas = suspectEgress
        cantSospechosas = len(sospechosas)
        Sospechosas = int(((cantSospechosas)/cantTotal)*100)

        Ok = int(((cantTotal - cantSospechosas)/cantTotal)*100)

        reportStatistics = {
            "Sospechosas": Sospechosas, 
            "Ok": Ok 
        }
        return reportStatistics

    def generateWeekReport(self, pk_days):
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)
        #filtro de deteccion de mes
        #filtro de deteccion de año, se muestran por mes
        Sospechosas=0

        listLastDaysWeek = []
        listOk = []
        listSospechosas = []

        listLastDaysMonth = ["4 semanas","3 semanas","2 semanas","1 semana"]
        listOkMonth = []
        listSospechosasMonth = [] 
        cantSospechosasSemanal= 0
        cantOkSemanal= 0

        listLastDaysYear= ["12 meses","11 meses","10 meses","9 meses","8 meses","7 meses","6 meses","5 meses","4 meses","3 meses","2 meses","1 mes"]
        listOkYear = []
        listSospechosasYear = [] 
        cantSospechosasMensual= 0
        cantOkMensual= 0

        count=0
        for i in range(pk_days):
            count= i+1
            #busco desde el día más viejo
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            listLastDaysWeek.append(toDate.strftime("%d/%m/%Y"))
            

            totales = self.stayDao.filter({"dateCreated__lte": toDate, 
                                          "dateCreated__gte": fromDate})
            cantTotal= 0
            cantSospechosas= 0
            cantTotal = len(totales)

            for estadia in totales:
                sospechosa = self.notificationEgressDao.filter({"isSuspected__exact": True, "estadia__exact": estadia})
                if(len(sospechosa)>=1):
                    cantSospechosas= cantSospechosas +1

            if(cantTotal==0):
                Sospechosas=0
                Ok=0
            else:
                if(cantSospechosas != 0):
                    Sospechosas=cantSospechosas
                    Ok= cantTotal - cantSospechosas

                    cantSospechosasSemanal= cantSospechosasSemanal + Sospechosas
                    cantOkSemanal= cantOkSemanal + Ok

                    cantSospechosasMensual= cantSospechosasMensual + Sospechosas
                    cantOkMensual= cantOkMensual + Ok
                else:
                    Ok=cantTotal
                    cantOkSemanal= cantOkSemanal + cantTotal
                    cantOkMensual= cantOkMensual + cantTotal
                    
            #Mensual
            if(count%7==0):
                listOkMonth.append(cantOkSemanal)
                listSospechosasMonth.append(cantSospechosasSemanal)
                cantSospechosasSemanal=0
                cantOkSemanal=0

            #Anual
            if(count%30==0):
                listOkYear.append(cantOkMensual)
                listSospechosasYear.append(cantSospechosasMensual)
                cantSospechosasMensual=0
                cantOkMensual=0

            listSospechosas.append(Sospechosas)
            listOk.append(Ok)

        if(pk_days < 30):
            reportStatistics = {
                "listaFechas": listLastDaysWeek,
                "listaSospechosas": listSospechosas, 
                "listaOk": listOk 
            }
        if(pk_days == 30):
            reportStatistics = {
                "listaFechas": listLastDaysMonth,
                "listaSospechosas": listSospechosasMonth, 
                "listaOk": listOkMonth 
            }
        if(pk_days == 360):
            reportStatistics = {
                "listaFechas": listLastDaysYear,
                "listaSospechosas": listSospechosasYear, 
                "listaOk": listOkYear 
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
            day1= pk-i
            day2= pk-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales = self.segmentDao.filter({"dateCreated__lte": toDate, 
                                              "dateCreated__gte": fromDate,
                                              "segmentType__exact": "SALIDA"})

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
                sospechosa = self.notificationEgressDao.filter({"isSuspected__exact": True, "estadia__exact": segment.estadia})

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

            listLastDaysWeek.append(toDate.strftime("%d/%m"+str(" Mañana")))
            listLastDaysWeek.append(toDate.strftime("%d/%m"+str(" Tarde")))
            listLastDaysWeek.append(toDate.strftime("%d/%m"+str(" Noche")))

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

    def valdateListNotEmpty(self):
        if(len(ReportService.listEntranceLunes)==0):
            ReportService.listEntranceLunes.append(0)
        if(len(ReportService.listEntranceMartes)==0):
            ReportService.listEntranceMartes.append(0)
        if(len(ReportService.listEntranceMiercoles)==0):
            ReportService.listEntranceMiercoles.append(0)
        if(len(ReportService.listEntranceJueves)==0):
            ReportService.listEntranceJueves.append(0)
        if(len(ReportService.listEntranceViernes)==0):
            ReportService.listEntranceViernes.append(0)
        if(len(ReportService.listEntranceSabado)==0):
            ReportService.listEntranceSabado.append(0)

        if(len(ReportService.listEgressLunes)==0):
            ReportService.listEgressLunes.append(0)
        if(len(ReportService.listEgressMartes)==0):
            ReportService.listEgressMartes.append(0)
        if(len(ReportService.listEgressMiercoles)==0):
            ReportService.listEgressMiercoles.append(0)
        if(len(ReportService.listEgressJueves)==0):
            ReportService.listEgressJueves.append(0)
        if(len(ReportService.listEgressViernes)==0):
            ReportService.listEgressViernes.append(0)
        if(len(ReportService.listEgressSabado)==0):
            ReportService.listEgressSabado.append(0)

    def cleanListDaysEntranceAndEgress(self):
        ReportService.listEntranceLunes = []
        ReportService.listEntranceMartes = []
        ReportService.listEntranceMiercoles = []
        ReportService.listEntranceJueves = []
        ReportService.listEntranceViernes = []
        ReportService.listEntranceSabado = []
        ReportService.listEgressLunes = []
        ReportService.listEgressMartes = []
        ReportService.listEgressMiercoles = []
        ReportService.listEgressJueves = []
        ReportService.listEgressViernes = []
        ReportService.listEgressSabado = []

    #Se asume que un usuario puede tener solo 1 estadía por día
    def findUserEstadiaReport(self, pk, pk_days):
        #pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)

        listDaysWeek = ["LU","MA","MI","JU","VI","SA"]
        #general
        listEntrance = []
        listEgress = []

        for i in range(pk_days):
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            estadiaUser = self.stayDao.filter({"dateCreated__lte": toDate, 
                                               "dateCreated__gte": fromDate,
                                               "userName__exact": pk})
            
            if(len(estadiaUser) == 1):
                segmentUserList = self.segmentDao.filter({"segmentType__exact": "SALIDA",
                                          "estadia__exact": estadiaUser[0]})
                
                segmentUser = segmentUserList[0] if len(segmentUserList)>0 else None

                if(segmentUser is not None):
                    horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
                    horaEgreso= int(segmentUser.dateCreated.strftime("%H"))

                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Monday"): 
                        ReportService.listEntranceLunes.append(horaIngreso)
                        ReportService.listEgressLunes.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Tuesday"): 
                        ReportService.listEntranceMartes.append(horaIngreso)
                        ReportService.listEgressMartes.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Wednesday"): 
                        ReportService.listEntranceMiercoles.append(horaIngreso)
                        ReportService.listEgressMiercoles.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Thursday"): 
                        ReportService.listEntranceJueves.append(horaIngreso)
                        ReportService.listEgressJueves.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Friday"): 
                        ReportService.listEntranceViernes.append(horaIngreso)
                        ReportService.listEgressViernes.append(horaEgreso)
                    if(segmentUser.estadia.dateCreated.strftime("%A")=="Saturday"): 
                        ReportService.listEntranceSabado.append(horaIngreso)
                        ReportService.listEgressSabado.append(horaEgreso)
                else:
                    print("La estadia no tiene cargada el segmento de Salida")
        #Validación de listas NO vacías
        self.valdateListNotEmpty()

        #ingresos por dias
        Ilu = Counter(ReportService.listEntranceLunes)
        Ima = Counter(ReportService.listEntranceMartes)
        Imi = Counter(ReportService.listEntranceMiercoles)
        Iju = Counter(ReportService.listEntranceJueves)
        Ivi = Counter(ReportService.listEntranceViernes)
        Isa = Counter(ReportService.listEntranceSabado)
        #lista final de ingresos
        listEntrance.append("Ingresos: ")
        listEntrance.append(max(Ilu, key=Ilu.get))
        listEntrance.append(max(Ima, key=Ima.get))
        listEntrance.append(max(Imi, key=Imi.get))
        listEntrance.append(max(Iju, key=Iju.get))
        listEntrance.append(max(Ivi, key=Ivi.get))
        listEntrance.append(max(Isa, key=Isa.get))

        #egresos por dias
        Olu = Counter(ReportService.listEgressLunes)
        Oma = Counter(ReportService.listEgressMartes)
        Omi = Counter(ReportService.listEgressMiercoles)
        Oju = Counter(ReportService.listEgressJueves)
        Ovi = Counter(ReportService.listEgressViernes)
        Osa = Counter(ReportService.listEgressSabado)
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
        self.cleanListDaysEntranceAndEgress()
        lista = []
        lista.append(reportStatistics3)
        lista.append(reportStatistics4)
        return lista

########################################################################

    #Se asume que por cada dia hay muchos ingresos y egresos
    def findAllEstadiaReport(self, pk_days):
        #pk_days=7
        now = datetime.datetime.utcnow()
        lastWeek = now - datetime.timedelta(days=pk_days)


        listDaysWeek = ["LU","MA","MI","JU","VI","SA"]
        #general
        listEntrance = []
        listEgress = []

        for i in range(pk_days):
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales= self.segmentDao.filter({"dateCreated__lte": toDate, 
                                             "dateCreated__gte": fromDate,
                                             "segmentType__exact": "SALIDA"})
            for segmentUser in totales:
                horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
                horaEgreso= int(segmentUser.dateCreated.strftime("%H"))

                if(segmentUser.estadia.dateCreated.strftime("%A")=="Monday"): 
                    ReportService.listEntranceLunes.append(horaIngreso)
                    ReportService.listEgressLunes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Tuesday"): 
                    ReportService.listEntranceMartes.append(horaIngreso)
                    ReportService.listEgressMartes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Wednesday"): 
                    ReportService.listEntranceMiercoles.append(horaIngreso)
                    ReportService.listEgressMiercoles.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Thursday"): 
                    ReportService.listEntranceJueves.append(horaIngreso)
                    ReportService.listEgressJueves.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Friday"): 
                    ReportService.listEntranceViernes.append(horaIngreso)
                    ReportService.listEgressViernes.append(horaEgreso)
                if(segmentUser.estadia.dateCreated.strftime("%A")=="Saturday"): 
                    ReportService.listEntranceSabado.append(horaIngreso)
                    ReportService.listEgressSabado.append(horaEgreso)

        #Validación de listas NO vacías
        self.valdateListNotEmpty()

        #ingresos por dias
        Ilu = Counter(ReportService.listEntranceLunes)
        Ima = Counter(ReportService.listEntranceMartes)
        Imi = Counter(ReportService.listEntranceMiercoles)
        Iju = Counter(ReportService.listEntranceJueves)
        Ivi = Counter(ReportService.listEntranceViernes)
        Isa = Counter(ReportService.listEntranceSabado)
        #lista final de ingresos
        listEntrance.append(max(Ilu, key=Ilu.get))
        listEntrance.append(max(Ima, key=Ima.get))
        listEntrance.append(max(Imi, key=Imi.get))
        listEntrance.append(max(Iju, key=Iju.get))
        listEntrance.append(max(Ivi, key=Ivi.get))
        listEntrance.append(max(Isa, key=Isa.get))

        #egresos por dias
        Olu = Counter(ReportService.listEgressLunes)
        Oma = Counter(ReportService.listEgressMartes)
        Omi = Counter(ReportService.listEgressMiercoles)
        Oju = Counter(ReportService.listEgressJueves)
        Ovi = Counter(ReportService.listEgressViernes)
        Osa = Counter(ReportService.listEgressSabado)
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
        
        self.cleanListDaysEntranceAndEgress()
        return reportStatistics

########################################################################

    #Se asume que por cada dia hay muchos ingresos y egresos
    def findAllEstadiaSuspectedAndPeakTimeReport(self, pk_days):
        #pk_days=7
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
            day1= pk_days-i
            day2= pk_days-1-i
            fromDate = now - datetime.timedelta(days=day1)
            toDate = now - datetime.timedelta(days=day2)

            totales= self.segmentDao.filter({"dateCreated__lte": toDate, 
                                             "dateCreated__gte": fromDate,
                                             "segmentType__exact": "LLEGADA"})

            for segmentUser in totales:
                horaIngreso=int(segmentUser.estadia.dateCreated.strftime("%H"))
                horaEgreso= int(segmentUser.dateCreated.strftime("%H"))
                listaRangoDeUso= list(range(horaIngreso,horaEgreso+1))
                sospechosa = self.notificationEgressDao.filter({"isSuspected__exact": True,
                                                    "estadia__exact": segmentUser.estadia})

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
        
        return reportStatistics
