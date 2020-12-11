
import time
import datetime
from .reportService import ReportService
from ..daos import SegmentDao, BicycleParkingDao, PlaceDao, PendingStayDao
from ..daos import NotificationEgressDao, StayDao

class EstadiaService():

    def __init__(self):
        self.reportService = ReportService()
        self.segmentDao = SegmentDao()
        self.bicycleParkingDao = BicycleParkingDao()
        self.placeDao = PlaceDao()
        self.pendingStayDao = PendingStayDao()
        self.notificationEgressDao = NotificationEgressDao()
        self.stayDao = StayDao()
        
    def findAll(self):
        items = self.stayDao.getAll()
        return self.parseEstadias(items)
    
    def filter(self, filters):
        return self.stayDao.filter(filters)
            
    def findByFilters(self, filters, isSuspected):
        estadias = self.stayDao.filter(filters)
        staysFiltered = []
        if (isSuspected):
            for e in estadias:
                itemOk = len(self.notificationEgressDao.filter({"estadia__exact":e})) > 0
                if (itemOk):
                    staysFiltered.append(e)
        else:
            staysFiltered = estadias                       
        return self.parseEstadias(staysFiltered)

    def createAnonymousStay(self, arrivalMove):
        place= self.placeDao.filter({"placeNumber__exact": arrivalMove.placeNumber})[0]
        anonimo = self.stayDao.insert({"placeUsed": arrivalMove.placeNumber, 
                                        "userName": 'Anonimo',
                                        "isAnonymous": True,
                                        "place": place})

        self.segmentDao.insert({
            "segmentType": 'LLEGADA', 
            "photoPath": arrivalMove.pathPhoto, 
            "photoInBase64": arrivalMove.photoInBase64,
            "estadia": anonimo
        })
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
        place.occupied= True
        place.save()
        print('Estadia anonima creada')
    
    #solo el sgmento de salida (la estadia ya está creada)
    def createAnonymousStayOUT(self, departureMove, estadia):
        
        self.segmentDao.insert({
            "segmentType": 'SALIDA', 
            "photoPath": departureMove.pathPhoto, 
            "photoInBase64": departureMove.photoInBase64,
            "estadia": estadia
        })
        #buscar el lugar asociado y ponerlo en False, va a romper!! filtrar con placeNumber
        place= estadia.place
        place.occupied= False
        place.save()

        estadia.isActive = False
        estadia.save()
        print('Estadia anonima cerrada')
    
    def registerEntrance(self, data):
        # TODO chequear
        parking = self.bicycleParkingDao.getByFilters({"number__exact": data['parkingNumber']})
        place = self.placeDao.get({"placeNumber__exact":data['place'], "bicycleParking__exact": parking})
        stayCreated = self.stayDao.get({"place__exact":place,"isActive__exact":True})

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
        stayCreated = self.stayDao.get({"userName__exact":data['userName'],"isActive__exact":True})

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
            segments = self.segmentDao.findByFilters({"estadia__exact": est})
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
        estadiaSuspected = self.notificationEgressDao.filter({"isSuspected__exact":True})
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
        
        pending = self.pendingStayDao.get({"userName__exact":userName,"isActive__exact":True})

        if (pending is not None):
            status = 'PENDING'
            return {
                'status': status, 
                'parking': pending.stay.place.bicycleParking.description, 
                'place': pending.stay.place.placeNumber
            }
        else:
            stay = self.stayDao.filter({"userName__exact":userName,"isActive__exact":True})
            status = 'ENTRANCE_DONE' if len(stay) > 0 else 'WITH_OUT_STAY'
        
        return {'status': status}

    def desactiveOldEstadias(self):
        now = datetime.datetime.utcnow()
        totales = self.stayDao.filter({"isActive__exact": True})
        for estadia in totales:
            if(estadia.dateCreated.strftime("%x")!= now.strftime("%x")):
                estadia.isActive=False
                estadia.save()
                
    def get(self, filters):
        return self.stayDao.get(filters)