from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from ..serializers import SegmentSerializer, EstadiaSerializer, PendingStaySerializer
from ..models import Estadia, Segment, Place, BicycleParking, PendingStay, BikeOwner
from ..services.validator import Validator
from ..services import EstadiaService
from django.core import serializers
from django.contrib.auth.models import User
import json

class EstadiaView():

    @api_view(['GET'])
    def getAll(request):
        service = EstadiaService()
        return Response(service.findAll())

    # GET trae por id 
    @api_view(['GET'])
    def get(request, pk):
        
        tasks = Estadia.objects.get(id=pk)
        serializer = EstadiaSerializer(tasks, many=False)
        return Response(serializer.data)

    @api_view(['GET'])
    def find(request):
             
        userName = request.query_params.get('userName', None)
        isActive = request.query_params.get('isActive', None)
        filters = {}
                
        if (userName is not None):
            filters['userName__exact'] = userName  
        if (isActive is not None):
            filters['isActive__exact'] = isActive.lower() == 'true'

        try:
            items = Estadia.objects.get(**filters)
            serializer = EstadiaSerializer(items, many=False)
            return Response(serializer.data)
        except Estadia.DoesNotExist:
            return Response({'message': 'Error Stay Not Found.'}, status=status.HTTP_404_NOT_FOUND)
            

    #Descripcion de cada bicicletero
    @api_view(['GET'])
    def getStateBike(request, pk):
        estadia = Estadia.objects.get(userName=pk, isActive=True) #asumo que hay 1 estadía por persona por día        
        places = Place.objects.filter(placeNumber = estadia.placeUsed)#asumo los lugares son únicos
        stateBike = {
            "description": places[0].bicycleParking.description, #descripcion del bicicletero
            "number": places[0].bicycleParking.number, #nunero de bicicletero
            "placeNumber": places[0].placeNumber #lugar del bicicletero
        }
        return Response(stateBike)

    @api_view(['POST'])
    def createStayEntrance(request):
        data = request.data
        print(data)
        service = EstadiaService()
        
        if (service.registerEntrance(data)):
            return Response("OK", status=status.HTTP_201_CREATED)                    
        else:
            return Response("Error al vincular entrada", status=status.HTTP_404_NOT_FOUND)
    
    
    @api_view(['POST'])
    def createStayEgress(request):
        data = request.data
        print(data)
        service = EstadiaService()
        
        if (service.registerEgress(data)):
            return Response("OK", status=status.HTTP_200_OK)                    
        else:
            return Response("Error al vincular entrada", status=status.HTTP_404_NOT_FOUND)
    
    
    @api_view(['POST'])
    def estadiaCreate(request):
        estadia = request.data
        validator = Validator()
        serializer = EstadiaSerializer(data=estadia)
        dataError = {}
        
        if serializer.is_valid():
            if validator.validateLocation():
                if validator.isValidSegment(estadia, "LLEGADA"):
                    estadiaSaved = serializer.save()
                    llegada = estadia['llegada']
                    Segment.objects.create(typeSegment='LLEGADA', 
                                        photoPath=llegada['photoPath'], 
                                        estadia=estadiaSaved)
                    print("Estadia creada exitosamente")
                else:
                    dataError = {'message': 'Error en estadia al generar la llegada'}                    
            else:
                dataError = {'message': 'location is not valid'}
        else:
            dataError = serializer.errors
        
        if dataError is not None:
            return Response(dataError, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @api_view(['PUT'])
    def estadiaUpdate(request, pk):
        estadia = Estadia.objects.get(id=pk)
        serializer = EstadiaSerializer(instance=estadia, data=request.data)
        validator = Validator()
        
        if serializer.is_valid() and validator.isValidSegment(request.data, "SALIDA"):
            serializer.save()
            salida = request.data['salida']
            Segment.objects.create(typeSegment='SALIDA', 
                                   photoPath=salida['photoPath'], 
                                   estadia=estadia)
            print("Salida para su estadia generada exitosamente")
        else:
            print("Error en estadia al generar la salida")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    
    ##localhost:8000/api/estadias?userName=pepe&isAnonymous=True
    
    @api_view(['GET'])
    def findEstadias(request):
        service = EstadiaService()
        
        toDate = request.query_params.get('toDate', None)
        fromDate = request.query_params.get('fromDate', None)
        userName = request.query_params.get('userName', None)
        isAnonymous = request.query_params.get('isAnonymous', None)
        isActive = request.query_params.get('isActive', None)
        
        filters = {}
        
        if (fromDate is not None):
            filters['dateCreated__gte'] = fromDate
            
        if (toDate is not None):
            filters['dateCreated__lte'] = toDate
        
        if (userName is not None):
            filters['userName__exact'] = userName  
        
        if (isAnonymous is not None):
            filters['isAnonymous'] = isAnonymous
        
        if (isActive is not None):
            filters['isActive__exact'] = isActive.lower() == 'true'
                        
        result = service.findByFilters(filters)
        return Response(result)

    
    @api_view(['GET'])
    def getPendingsStays(request):

        userName = request.query_params.get('userName', None)
        
        filters = {}
        
        if (userName is not None):
            filters['userName__exact'] = userName

        items = PendingStay.objects.filter(**filters)

        response = []
        
        for i in items:
            place=i.stay.place
            entrance = Segment.objects.get(estadia=i.stay)
            user = User.objects.get(username=i.userName)
            bikeOwner = BikeOwner.objects.get(user=user)
            item = {
              'userName': i.userName,
              'dateCreated': i.dateCreated,
              'place': place.placeNumber,
              'isAuthorize': i.isAuthorize,
              'bicycleParking': {
                'number': place.bicycleParking.number,
                'description': place.bicycleParking.description              
              },
              'photos': {
                'user': bikeOwner.profilePhoto,
                'entrance': entrance.photoPath,
              }
            }
            response.append(item)

        return Response(response)


    @api_view(['POST'])    
    def authorize(request):
        userName = request.data['userName']
        isAuthorize = request.data['isAuthorize']
        
        pendingStay = PendingStay.objects.get(userName=userName)
        pendingStay.isAuthorize = isAuthorize

        stay = pendingStay.stay
        if (isAuthorize):
            stay.userName = userName
            stay.isAnonymous = False
        else:
            stay.userName = 'Anonimo'
            stay.isAnonymous = True

        stay.save()
        pendingStay.save()        
        return Response(status=status.HTTP_200_OK)


    @api_view(['GET'])
    def findEstadiasReportes(request):
        #hacre un JSON a mano
        #buscar en estadias y separarlos en 2
        #cantidad de estadias sospechosas (tienen notication egress y yes en isSuspected)
        #cantidad de estadias no sospechosas (no tiene notication egress y no en isSuspected)
        #cantidad de estadias totales
        #hacer pruebas con los registros
        #luego filtrar
        service = EstadiaService()
        cantTotal= 0
        cantSospechosas= 0
        cantOk= 0

        totales = service.findAll()
        cantTotal = len(totales)
        print("cantTotal: ",cantTotal)

        sospechosas= service.findSuspectEgress()
        cantSospechosas= len(sospechosas)
        Sospechosas=int(((cantSospechosas)/cantTotal)*100)
        print("Sospechosas: ",Sospechosas)

        Ok= int(((cantTotal - cantSospechosas)/cantTotal)*100)
        print("Ok: ",Ok)

        reportStatistics = {
            "Sospechosas": Sospechosas, 
            "Ok": Ok 
        }
        print(reportStatistics)
        return Response(reportStatistics)
