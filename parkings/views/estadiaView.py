from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from ..serializers import SegmentSerializer, EstadiaSerializer
from ..models import Estadia, Segment, Place
from ..services.validator import Validator
from ..services import EstadiaService
from django.core import serializers
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
    def getUser(request, pk):
        tasks = Estadia.objects.get(userName=pk)
        serializer = EstadiaSerializer(tasks, many=False)
        return Response(serializer.data)
    

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
        
        filters = {}
        
        if (fromDate is not None):
            filters['dateCreated__gte'] = fromDate
            
        if (toDate is not None):
            filters['dateCreated__lte'] = toDate
        
        if (userName is not None):
            filters['userName__exact'] = userName  
        
        if (isAnonymous is not None):
            filters['isAnonymous'] = isAnonymous
                    
        result = service.findByFilters(filters)
        return Response(result)
    