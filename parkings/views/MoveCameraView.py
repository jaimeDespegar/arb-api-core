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
                    print("es egreso no se creo nada")
                    
                    estadiaFinal = Estadia.objects.filter(placeUsed= moveSaved.placeNumber)[0]
                    service.createAnonymousStayOUT(moveSaved, estadiaFinal)
                    #poner en ocupado en False
            
                    NotificationEgress.objects.create(userName='userName',photoPath=moveSaved.pathPhoto,
                    place= moveSaved.placeNumber, isOk = False, isSuspected = True, estadia=estadiaFinal)
                else:
                    service.createAnonymousStay(moveSaved)
                    print("estadia anonima, ingreso")
                    
                responseData.append(serializer.data)
                
                    
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED)


    # def checkSuspectedMove():
    #     tolerancia= 5 #segundos
    #     exitMoves= MoveCamera.objects.filter(occupied=False,registered=False)#busco en la tabla

    #     for move in exitMoves:
    #         notification = Notification.objects.get(placeNumber= move.placeNumber)
            
    #         isNotAlarmActive = (notification == None) #boolean , None=null

    #         now = time.time()
    #         diferencia= int(now - move.createDate)
    #         if(diferencia>=tolerancia and (isNotAlarmActive)):
    #             Notification.objects.create(userName='userName',photoPath=move.pathPhoto, place= move.placeNumber)
    #             print("ALARMA!")


    #@api_view(['GET', 'POST', 'PUT'])
    #def parkings_list(request):
    #    return JsonResponse({}, safe=False)
        # if request.method == 'GET':
        #     parkings = Parkings.objects.all()
        #     serializer = ParkingsSerializer(parkings, many=True)
        #     return JsonResponse(serializer.data, safe=False)

        # elif request.method == 'POST' and not 'parkings' in request.data:
        #     serializer = ParkingsSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # elif request.method == 'POST' and 'parkings' in request.data:
        #     data = request.data['parkings']
        #     responseData = []
        #     for parking in data:
        #         print(parking)
        #         serializer = ParkingsSerializer(data=parking)
        #         if serializer.is_valid():
        #             serializer.save()
        #             responseData.append(serializer.data)
        #         else:
        #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     return Response(responseData, status=status.HTTP_201_CREATED)

        # elif request.method == 'PUT' and 'parkings' in request.data:
        #     data = request.data['parkings']
        #     responseData = []
        #     for parking in data:
        #         try:
        #             parkingOld = Parkings.objects.get(pk=int(parking['id']))
        #         except Parkings.DoesNotExist:
        #             return Response(status=status.HTTP_404_NOT_FOUND)
        #         serializer = ParkingsSerializer(parkingOld, data=parking)
        #         if serializer.is_valid():
        #             serializer.save()
        #             responseData.append(serializer.data)
        #         else:
        #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     return Response(responseData, status=status.HTTP_201_CREATED)

    # @api_view(['GET', 'PUT', 'DELETE'])
    # def parking_detail(request, pk):
        # try:
        #     parking = Parkings.objects.get(pk=pk)
        # except Parkings.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        # if request.method == 'GET':
        #     serializer = ParkingsSerializer(parking)
        #     return Response(serializer.data)

        # elif request.method == 'PUT':
        #     serializer = ParkingsSerializer(parking, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # elif request.method == 'DELETE':
        #     parking.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
