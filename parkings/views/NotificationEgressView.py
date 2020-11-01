from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import NotificationEgressSerializer
from ..models.notificationEgress import NotificationEgress

class NotificationEgressView():

    @api_view(['GET'])
    def notificationEgressGet(request, pk):
        tasks = NotificationEgress.objects.get(id=pk)
        serializer = NotificationEgressSerializer(tasks, many=False)
        return Response(serializer.data)

   # GET trae todas (para el guardia)
    @api_view(['GET'])
    def notificationEgressGetAll(request):
        tasks = NotificationEgress.objects.all()
        serializer = NotificationEgressSerializer(tasks, many=True)
        return Response(serializer.data)


    @api_view(['PUT'])
    def notificationEgressUpdate(request, pk):
        notifEgress = NotificationEgress.objects.get(id=pk)
        notifEgress.isSuspected=request.data["isSuspected"]
        notifEgress.save()
        ##Response({"key": item.data})
        return Response("ok")
