from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import BicycleParkingSerializer
from ..services.bicycleParkingService import BicycleParkingService

class BicycleParkingView():

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
    
    @api_view(['GET'])
    def getAllBicycleParking(request):
        tasks = BicycleParkingService.getAll()
        serializer = BicycleParkingSerializer(tasks, many=True)
        return Response(serializer.data)


    @api_view(['GET'])
    def getBicycleParking(request, pk):
        tasks = BicycleParkingService.get({"id__exact":pk})
        serializer = BicycleParkingSerializer(tasks, many=False)
        return Response(serializer.data)

    @api_view(['GET'])
    def bicycleParkingAvailability(request):
        freePlaces = BicycleParkingService.getCountFreePlaces()        
        return Response(freePlaces)

    @api_view(['PUT'])
    def updateBicicleParking(request):
        parking = BicycleParkingService.get({"number__exact": request.data['number']})
        serializer = BicycleParkingSerializer(instance=parking, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print("Modificación de descripcion de bicicletero exitoso")
        else:
            print("Error al modificar descripcion del bicicletero")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @api_view(['DELETE'])
    def bicicleParkingDelete(request, number):
        parking = BicycleParkingService.get({"number__exact": number})
        parking.delete()
        return Response("Parking borrado satisfactoriamente", status=status.HTTP_200_OK)

    @api_view(['GET'])
    def getAllBicyclesParkings(request):
        tasks = BicycleParkingService.getAllBicycleParkingAndPlaces()
        return Response(tasks, status=status.HTTP_200_OK)