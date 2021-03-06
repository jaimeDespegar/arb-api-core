from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import SegmentSerializer, EstadiaSerializer
from ..services import EstadiaService, SegmentService
from django.core import serializers


class EstadiaView():

    @api_view(['GET'])
    def getAll(request):
        service = EstadiaService()
        return Response(service.findAll())

    @api_view(['GET'])
    def find(request):
             
        userName = request.query_params.get('userName', None)
        isActive = request.query_params.get('isActive', None)
        filters = {}
                
        if (userName is not None):
            filters['userName__exact'] = userName  
        if (isActive is not None):
            filters['isActive__exact'] = isActive.lower() == 'true'

        items = EstadiaService().get(filters)
        if (items is not None):
            serializer = EstadiaSerializer(items, many=False)
            return Response(serializer.data)
        else :
            return Response({'message': 'Error Stay Not Found.'}, status=status.HTTP_404_NOT_FOUND)
            

    @api_view(['GET'])
    def getStateBike(request, pk):
        estadia = EstadiaService().get({"userName__exact":pk, "isActive__exact":True})
        if (estadia is not None):
            segment = SegmentService().get({"estadia__exact":estadia, "segmentType__exact":'LLEGADA'})
                        
            place = estadia.place
            stateBike = {
                "description": place.bicycleParking.description,
                "number": place.bicycleParking.number,
                "placeNumber": place.placeNumber,
                "photo": segment.photoInBase64 if segment is not None else ''
            }
            return Response(stateBike)
        else:
            return Response({'message': 'Error Stay Not Found.'}, status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def createStayEntrance(request):
        service = EstadiaService()
        
        if (service.registerEntrance(request.data)):
            return Response("OK", status=status.HTTP_201_CREATED)                    
        else:
            return Response("Error al vincular entrada", status=status.HTTP_404_NOT_FOUND)
    
    
    @api_view(['POST'])
    def createStayEgress(request):
        service = EstadiaService()
        
        if (service.registerEgress(request.data)):
            return Response("OK", status=status.HTTP_200_OK)                    
        else:
            return Response("Error al vincular salida", status=status.HTTP_404_NOT_FOUND)
        
    
    @api_view(['GET'])
    def findEstadias(request):
        service = EstadiaService()
        
        toDate = request.query_params.get('toDate', None)
        fromDate = request.query_params.get('fromDate', None)
        userName = request.query_params.get('userName', None)
        isAnonymous = request.query_params.get('isAnonymous', None)
        isActive = request.query_params.get('isActive', None)
        isSuspected = request.query_params.get('isSuspected', None)
        
        filters = {}
        
        if (fromDate is not None):
            filters['dateCreated__gte'] = fromDate #mayor e igual
            
        if (toDate is not None):
            filters['dateCreated__lte'] = toDate #menor e igual
        
        if (userName is not None):
            filters['userName__exact'] = userName #igual
        
        if (isAnonymous is not None):
            filters['isAnonymous__exact'] = isAnonymous
            
        if (isActive is not None):
            filters['isActive__exact'] = isActive.lower() == 'true'
        
        result = service.findByFilters(filters, isSuspected)
        return Response(result)


    @api_view(['GET'])
    def findEstadiasReportes(request):
        service = EstadiaService()
        reportStatistics = service.buildReportStatistics()
        return Response(reportStatistics)


    @api_view(['GET'])
    def findEstadiasReportesSemanal(request,pk_days):
        service = EstadiaService()
        print("pk_days: ",pk_days)
        data = service.generateWeekReport(pk_days)
        return Response(data)

    @api_view(['GET'])
    def findEstadiasReportesRango(request, pk):
        service = EstadiaService()
        data = service.generateAllEstadiaReport(pk)
        return Response(data)

    @api_view(['GET'])
    def findPromedioHourUserEstadiaWeekReportes(request):
        service = EstadiaService()
        data = service.findPromedioHourEstadiaReport()
        return Response(data)

    @api_view(['GET'])
    def findHourUserEstadiaWeekReportes(request, pk, pk_days):
        service = EstadiaService()
        data = service.findUserEstadiaReport(pk,pk_days)
        return Response(data)

    @api_view(['GET'])
    def findHourAllEstadiaWeekReportes(request, pk_days):
        service = EstadiaService()
        data = service.findAllEstadiaReport(pk_days)
        return Response(data)

    @api_view(['GET'])
    def findHourAllSuspectedAndPeakTime(request, pk_days):
        service = EstadiaService()
        data = service.findAllEstadiaSuspectedAndPeakTimeReport(pk_days)
        return Response(data)

    @api_view(['GET'])
    def getStatusStayByUser(request):
        service = EstadiaService()
        userName = request.query_params.get('userName', None)
        data = service.getStatusStay(userName)
        return Response(data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def cleanOldStadias(request):
        service = EstadiaService()
        data = service.desactiveOldEstadias()
        return Response(data, status=status.HTTP_200_OK)
