
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import UserSerializer, BikeOwnerSerializer, CreateUserSerializer
from ..models.user import BikeOwner
from django.contrib.auth.models import User


class RegisterUserView():

    #Registro BikeOwner
    @api_view(['POST'])
    def registerBikeOwnerCreate(request):
        data = request.data
        responseData = []

        serializer = BikeOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responseData.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED) 

    # GET trae todas 
    @api_view(['GET'])
    def registerBikeOwnerGetAll(request):
        tasks = BikeOwner.objects.all()
        serializer = BikeOwnerSerializer(tasks, many=True)
        return Response(serializer.data)
    
    # GET trae por id 
    @api_view(['GET'])
    def registerBikeOwnerGet(request, pk):
        tasks = BikeOwner.objects.get(id=pk)
        serializer = BikeOwnerSerializer(tasks, many=False)
        return Response(serializer.data)

    # GET trae por id 
    @api_view(['GET'])
    def registerBikeOwnerGetUser(request, pk):
        user = User.objects.get(username=pk)
        owner = BikeOwner.objects.get(user=user)
        userResponse = {
            'userName': user.username,
            "email": user.email,
            "bicyclePhoto": owner.bicyclePhoto,
            "profilePhoto": owner.profilePhoto,
            "password": user.password,
            "pet": owner.pet,
            "street": owner.street,
            "movie": owner.movie,
        }
        return Response(userResponse)
    
    #servicio para que el usuario modifique sus datos de reistro
    @api_view(['PUT'])
    def registerBikeOwnerUpdateUser(request, pk):

        userEdited = request.data

        user = User.objects.get(username=pk)
        bikeOwner = BikeOwner.objects.get(user=user)
        user.email = userEdited["email"]
        user.set_password(userEdited["password"])
        user.save()
        
        bikeOwner.bicyclePhoto = userEdited['bicyclePhoto']
        bikeOwner.profilePhoto = userEdited['profilePhoto']
        # bikeOwner.pet = userEdited['pet']
        # bikeOwner.street = userEdited['street']
        # bikeOwner.movie = userEdited['movie']
        bikeOwner.save()
                
        return Response(userEdited, status=status.HTTP_200_OK)

    @api_view(['DELETE'])
    def bikeOwnerDelete(request, pk):
        print('request data ' + str(pk))
        user = User.objects.get(userName=pk)
        user.delete()
        return Response("user borrado satisfactoriamente")