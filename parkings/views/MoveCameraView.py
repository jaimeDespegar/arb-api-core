from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import MovesSerializer
import time
from ..models import MoveCamera, NotificationEgress, Estadia
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
                    place= moveSaved.placeNumber, isOk = False, estadia=estadiaFinal)
                else:
                    service.createAnonymousStay(moveSaved)
                    
                responseData.append(serializer.data)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED)
