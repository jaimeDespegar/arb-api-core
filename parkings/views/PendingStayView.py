from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Segment, PendingStay, BikeOwner 
from django.contrib.auth.models import User


class PendingStayView():
        
    @api_view(['GET'])
    def getPendingsStays(request):

        userName = request.query_params.get('userName', None)
        
        filters = {}
        
        if (userName is not None):
            filters['userName__exact'] = userName

        items = PendingStay.objects.filter(**filters)

        response = []
        
        for i in items:
            place=i.stay.place
            entrance = Segment.objects.get(estadia=i.stay, segmentType='LLEGADA')
            user = User.objects.get(username=i.userName)
            bikeOwner = BikeOwner.objects.get(user=user)
            item = {
              'userName': i.userName,
              'dateCreated': i.dateCreated,
              'place': place.placeNumber,
              'isAuthorize': i.isAuthorize,
              'bicycleParking': {
                'number': place.bicycleParking.number,
                'description': place.bicycleParking.description              
              },
              'photos': {
                'user': bikeOwner.profilePhoto,
                'entrance': entrance.photoPath,
              }
            }
            response.append(item)

        return Response(response)


    @api_view(['POST'])    
    def authorize(request):
        userName = request.data['userName']
        isAuthorize = request.data['isAuthorize']
        
        pendingStay = PendingStay.objects.get(userName=userName)
        pendingStay.isAuthorize = isAuthorize

        stay = pendingStay.stay
        if (isAuthorize):
            stay.userName = userName
            stay.isAnonymous = False
        else:
            stay.userName = 'Anonimo'
            stay.isAnonymous = True

        stay.save()
        pendingStay.save()        
        return Response(status=status.HTTP_200_OK)
