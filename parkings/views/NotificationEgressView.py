from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import NotificationEgressSerializer
from ..models.notificationEgress import NotificationEgress
from ..services import EstadiaService


class NotificationEgressView():

    @api_view(['GET'])
    def notificationEgressGet(request, pk):
        tasks = NotificationEgress.objects.get(id=pk)
        serializer = NotificationEgressSerializer(tasks, many=False)
        return Response(serializer.data)

    # GET trae por userName 
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

   # GET trae todas (para el guardia)
    @api_view(['GET'])
    def notificationEgressGetAll(request):
        tasks = NotificationEgress.objects.all()
        serializer = NotificationEgressSerializer(tasks, many=True)
        return Response(serializer.data)

    # histarial de robos 
    @api_view(['GET'])
    def notificationEgressHistorySuspectedGet(request):
        tasks= NotificationEgress.objects.filter(isSuspected= "True")
        serializer = NotificationEgressSerializer(tasks, many=True)
        return Response(serializer.data)

    @api_view(['PUT'])
    def notificationEgressUpdate(request, pk):
        notifEgress = NotificationEgress.objects.get(id=pk)
        notifEgress.isSuspected=request.data["isSuspected"]
        notifEgress.save()
        ##Response({"key": item.data})
        return Response("ok")

    #Actualiza el estados de casos sospechosos buscando por nombre de usuario
    @api_view(['PUT'])
    def notificationEgressUpdateUser(request, pk):
        notifEgress = NotificationEgress.objects.get(userName=pk)
        notifEgress.isSuspected=request.data["isSuspected"]
        notifEgress.isActive=request.data["isActive"]
        notifEgress.save()
        service = EstadiaService()
        egressSuccess = service.registerEgress(request.data)
        print('register egress success ' + egressSuccess)
        return Response("OK", status=status.HTTP_200_OK)
