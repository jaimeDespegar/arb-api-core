from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from ..serializers import NotificationSerializer
from ..models.notification import Notification

class NotificationView():

    @api_view(['POST'])
    def notificationMoveCreate(request):
        data = request.data['users']
        responseData = []
        for user in data:
            serializer = NotificationSerializer(data=user)
            if serializer.is_valid():
                serializer.save()
                responseData.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responseData, status=status.HTTP_201_CREATED)


    @api_view(['GET'])
    def notificationGet(request, pk):
        tasks = Notification.objects.get(id=pk)
        serializer = NotificationSerializer(tasks, many=False)
        return Response(serializer.data)