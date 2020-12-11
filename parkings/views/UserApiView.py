
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from ..serializers import CreateUserSerializer
from ..services import UserService


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        service = UserService()
        newUser = request.data

        olduser = service.getUser({"username__exact": newUser['username']})

        if (olduser is not None):
            return Response("Error el usuario ya existe", status=status.HTTP_404_NOT_FOUND)#status=status.HTTP_501_NOT_IMPLEMENTED)

        oldmail = service.getUser({"email__exact": newUser['email']})
        
        if (oldmail is not None):
            return Response("Error el email ya existe", status=status.HTTP_404_NOT_FOUND)#status=status.HTTP_503_SERVICE_UNAVAILABLE)

        serializer = self.get_serializer(data=newUser)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
    
        headers = self.get_success_headers(serializer.data)

        # create bikeowner
        service.createBikeOwner({"bicyclePhoto": newUser['bicyclePhoto'],
                                 "profilePhoto": newUser['profilePhoto'],
                                 "pet": newUser['pet'],
                                 "street": newUser['street'],
                                 "movie": newUser['movie'],
                                 "user": serializer.instance})
        
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
