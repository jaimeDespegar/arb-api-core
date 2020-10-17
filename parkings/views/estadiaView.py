from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import MovesSerializer, EstadiaSerializer
from ..models import Estadia

class EstadiaView():

    @api_view(['GET'])
    def getAll(request):
        tasks = Estadia.objects.all()
        serializer = EstadiaSerializer(tasks, many=True)
        return Response(serializer.data)


    @api_view(['POST'])
    def estadiaCreate(request):
        serializer = EstadiaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    

    @api_view(['PUT'])
    def estadiaUpdate(request, user):
        task = Estadia.objects.get(id=user)
        serializer = EstadiaSerializer(instance=task, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    