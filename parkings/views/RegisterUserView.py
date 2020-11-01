# reutilizar componente REgister
# los datos los voy a buscar a la api
# crear un url GET que te traiga los datos del usuario

from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import UserSerializer, BikeOwnerSerializer
#from ..models.user import User
from ..models.user import BikeOwner

class RegisterUserView():

    # #Registro User
    # @api_view(['POST'])
    # def registerUserCreate(request):
    #     data = request.data
    #     responseData = []

    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         responseData.append(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(responseData, status=status.HTTP_201_CREATED) 

    # # GET trae todas 
    # @api_view(['GET'])
    # def registerUserGetAll(request):
    #     tasks = User.objects.all()
    #     serializer = UserSerializer(tasks, many=True)
    #     return Response(serializer.data)
    
    # # GET trae por id 
    # @api_view(['GET'])
    # def registerUserGet(request, pk):
    #     tasks = User.objects.get(id=pk)
    #     serializer = UserSerializer(tasks, many=False)
    #     return Response(serializer.data)


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
        tasks = BikeOwner.objects.get(userName=pk)
        serializer = BikeOwnerSerializer(tasks, many=False)
        return Response(serializer.data)

    #servicio para que el usuario modifique sus datos de reistro
    @api_view(['PUT'])
    def registerBikeOwnerUpdate(request, pk):
        parking = BikeOwner.objects.get(id=pk)
        serializer = BikeOwnerSerializer(instance=parking, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print("Modificación de datos de usuario exitoso")
        else:
            print("Error al modificar  datos de usuario")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    
    
    #servicio para que el usuario modifique sus datos de reistro
    @api_view(['PUT'])
    def registerBikeOwnerUpdateUser(request, pk):
        parking = BikeOwner.objects.get(userName=pk)
        serializer = BikeOwnerSerializer(instance=parking, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print("Modificación de datos de usuario exitoso")
        else:
            print("Error al modificar  datos de usuario")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
