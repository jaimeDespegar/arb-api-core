from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import NotificationEgressSerializer
from ..services import EstadiaService, NotificationEgressService


class NotificationEgressView():

    @api_view(['GET'])
    def notificationEgressGetUser(request, pk):
        task = NotificationEgressService().get({"userName__exact": pk, "isActive__exact": True})
        if task is not None:
            serializer = NotificationEgressSerializer(task, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET'])
    def notificationEgressGetAll(request):
        tasks = NotificationEgressService().getAll()
        serializer = NotificationEgressSerializer(tasks, many=True)
        data = []
        for task in tasks:
            item = {
                "dateCreated": task.dateCreated,
                "isActive": task.isActive,
                "isSuspected": task.isSuspected,
                "photoInBase64": task.photoInBase64,
                "userName": task.userName,
                "place": task.estadia.place.placeNumber
            }
            data.append(item)
            
        return Response(data, status=status.HTTP_200_OK)

    @api_view(['PUT'])
    def notificationEgressUpdateUser(request, pk):
        notifEgress = NotificationEgressService().get({"userName__exact":pk, "isActive__exact":True})
        notifEgress.isSuspected=request.data["isSuspected"]
        notifEgress.isActive=request.data["isActive"]
        notifEgress.save()
        service = EstadiaService()
        egressSuccess = service.registerEgress(request.data)
        return Response("OK", status=status.HTTP_200_OK)