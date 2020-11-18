from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import NotificationEgressSerializer
from ..models.notificationEgress import NotificationEgress
from ..services import EstadiaService


class NotificationEgressView():

    @api_view(['GET'])
    def notificationEgressGetUser(request, pk):
        try:
            task = NotificationEgress.objects.get(userName=pk, isActive=True)
        except NotificationEgress.DoesNotExist:
            task = None    

        if task is not None:
            serializer = NotificationEgressSerializer(task, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET'])
    def notificationEgressGetAll(request):
        tasks = NotificationEgress.objects.all()
        serializer = NotificationEgressSerializer(tasks, many=True)
        return Response(serializer.data)

    #Actualiza el estados de casos sospechosos buscando por nombre de usuario
    @api_view(['PUT'])
    def notificationEgressUpdateUser(request, pk):
        notifEgress = NotificationEgress.objects.get(userName=pk, isActive=True)
        notifEgress.isSuspected=request.data["isSuspected"]
        notifEgress.isActive=request.data["isActive"]
        notifEgress.save()
        service = EstadiaService()
        egressSuccess = service.registerEgress(request.data)
        return Response("OK", status=status.HTTP_200_OK)