from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import MovesSerializer, BicycleParkingSerializer, PlaceSerializer
import time
from ..models import MoveCamera, NotificationEgress, Estadia, BicycleParking, Place
from ..services import EstadiaService


class MoveCameraView():

    @api_view(['POST'])
    def moveCreate(request):
        data = request.data['registers']
        responseData = []
        service = EstadiaService()
        for register in data:
            serializer = MovesSerializer(data=register)
            if serializer.is_valid():
                moveSaved = serializer.save()
                if (moveSaved.occupied): #Debería ser al revés!! ver en camera detection!                    
                    estadiaFinal = Estadia.objects.filter(placeUsed= moveSaved.placeNumber)[0]
                    service.createAnonymousStayOUT(moveSaved, estadiaFinal)
                    
                    NotificationEgress.objects.create(userName=estadiaFinal.userName,photoPath=moveSaved.pathPhoto,
                    place= moveSaved.placeNumber, estadia=estadiaFinal)
                else:
                    service.createAnonymousStay(moveSaved)
                    
                responseData.append(serializer.data)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED)

    @api_view(['POST'])
    def moveBicycleparkingCreate(request):
        data = request.data
        responseData = []

        serializer = BicycleParkingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responseData.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED)

    @api_view(['POST'])
    def movePlaceCreate(request):
        data = request.data
        responseData = []

        data0 = BicycleParking.objects.filter(number= 0)[0]
        print("BicycleParking: ")
        print(data0)


        datafinal = Place.objects.create(placeNumber=int(data), 
                                    occupied=False,
                                    bicycleParking=data0)
        print("Place: ")
        print(datafinal)

        #serializer = PlaceSerializer(data=datafinal)

        #print(serializer.is_valid())
        #if serializer.is_valid():
        #    serializer.save()
        #    responseData.append(serializer.data)
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED)
