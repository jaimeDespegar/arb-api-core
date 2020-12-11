from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import UserSerializer, BikeOwnerSerializer, CreateUserSerializer
from ..services import UserService


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
        tasks = UserService().getAllBikeOwner()
        serializer = BikeOwnerSerializer(tasks, many=True)
        return Response(serializer.data)

    # GET trae todas 
    @api_view(['GET'])
    def parseBikeOwnerGetAll(request):
        owners = UserService().getAllBikeOwner()

        listBikeOwner = []
        
        for owner in owners:
            
            userResponse = {
            "username": owner.user.username,
            "email": owner.user.email,
            "bicyclePhoto": owner.bicyclePhoto,
            "profilePhoto": owner.profilePhoto,
            "pet": owner.pet,
            "street": owner.street,
            "movie": owner.movie,
            }
            
            listBikeOwner.append(userResponse)
            
        return Response(listBikeOwner)

    @api_view(['GET'])
    def parseBikeOwnerFind(request):
        username = request.query_params.get('user.username', None)#userName
        service = UserService()
        
        filters = {}

        if (username is not None):
            user = service.getUser({"username__exact": username})    
            if (user is not None):
                filters['user__exact'] = user

        owners = service.getBikeOwnerByFilters(filters)
        
        listBikeOwner = []
        
        for owner in owners:
            
            userResponse = {
            "username": owner.user.username,
            "email": owner.user.email,
            "bicyclePhoto": owner.bicyclePhoto,
            "profilePhoto": owner.profilePhoto,
            "pet": owner.pet,
            "street": owner.street,
            "movie": owner.movie,
            }
            
            listBikeOwner.append(userResponse)
        
        return Response(listBikeOwner)
    
    
    @api_view(['GET'])
    def registerBikeOwnerGetUser(request, pk):
        service = UserService()
        user = service.getUser({"username__exact": pk})
        owner = service.getBikeOwner({"user__exact": user})
        userResponse = {
            'username': user.username,
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
        service = UserService()
        
        user = service.getUser({"username__exact": pk})
        oldmail = service.getUser({"username__exact":pk, "email__exact":userEdited['email']})
                    
        if (oldmail == None):
            return Response("Error el email ya existe", status=status.HTTP_404_NOT_FOUND)#status=status.HTTP_503_SERVICE_UNAVAILABLE)

        bikeOwner = service.getBikeOwner({"user__exact": user})
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
        user = UserService().getUser({"username__exact": pk})
        user.delete()
        return Response("user borrado satisfactoriamente")