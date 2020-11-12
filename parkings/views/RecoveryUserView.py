from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import UserSerializer, BikeOwnerSerializer, CreateUserSerializer
from ..models.user import BikeOwner
from django.contrib.auth.models import User


class RecoveryUserView():
    #No sirve ya que se necesita el token o mandar mails!!
    @api_view(['PUT'])
    def recoveryBikeOwnerUpdateUser(request, pk):
        print("RecoveryUserView")

        userEdited = request.data

        user = User.objects.get(username=pk)
        bikeOwner = BikeOwner.objects.get(user=user)

        if(userEdited['petJoined'] == bikeOwner.pet ):
            if(userEdited['streetJoined'] == bikeOwner.street ):
                if(userEdited['movieJoined'] == bikeOwner.movie ):
                    user.set_password(pk)
                    user.save()

        
                
        return Response(userEdited, status=status.HTTP_200_OK)