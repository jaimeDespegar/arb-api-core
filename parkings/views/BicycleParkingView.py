from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import BicycleParkingSerializer
from ..models.bicycleParking import BicycleParking
from ..models.place import Place
from ..services.bicycleParkingService import BicycleParkingService


class BicycleParkingView():

    #Estacionar Bicicleta
    @api_view(['POST'])
    def bicycleParkingCreate(request):
        data = request.data
        responseData = []

        serializer = BicycleParkingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responseData.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED) 

    # GET trae todas (para el guardia)
    @api_view(['GET'])
    def bicycleParkingGetAll(request):
        tasks = BicycleParking.objects.all()
        serializer = BicycleParkingSerializer(tasks, many=True)
        return Response(serializer.data)
    
    # GET trae por id (para consultar el estadía actual)
    @api_view(['GET'])
    def bicycleParkingGet(request, pk):
        tasks = BicycleParking.objects.get(id=pk)
        serializer = BicycleParkingSerializer(tasks, many=False)
        return Response(serializer.data)


    @api_view(['GET'])
    def bicycleParkingAvailability(request):
        freePlaces = BicycleParkingService.getCountFreePlaces()        
        return Response({'freePlaces':freePlaces})