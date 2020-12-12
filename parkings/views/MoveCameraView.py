from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import MovesSerializer, BicycleParkingSerializer
from ..services import EstadiaService, BicycleParkingService, NotificationEgressService


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
                    stay = service.filter({"placeUsed__exact":moveSaved.placeNumber})[0]
                    service.createAnonymousStayOUT(moveSaved, stay)
                    
                    NotificationEgressService().create({"userName": stay.userName, 
                                                        "estadia": stay,
                                                        "photoInBase64": moveSaved.photoInBase64})
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
        service = BicycleParkingService()
        data0 = service.filter({"number__exact": 0})[0]
        print(data)
        datafinal = service.createPlace({"placeNumber": int(data), 
                                         "occupied": False,
                                         "bicycleParking": data0})

        return Response(responseData, status=status.HTTP_201_CREATED)