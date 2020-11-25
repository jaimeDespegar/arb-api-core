from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Segment, PendingStay, BikeOwner, Place, BicycleParking, Estadia 
from django.contrib.auth.models import User


class PendingStayView():
        
    @api_view(['GET'])
    def getPendingsStays(request):

        userName = request.query_params.get('userName', None)
        isActive = request.query_params.get('isActive', None)
        notifyToUser = request.query_params.get('notifyToUser', None)
        
        filters = {}
        
        if (userName is not None):
            filters['userName__exact'] = userName
            
        if (isActive is not None):
            filters['isActive__exact'] = isActive
            
        if (notifyToUser is not None):
            filters['notifyToUser__exact'] = notifyToUser
            
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
        stay = pendingStay.stay
        if (isAuthorize):
            stay.userName = userName
            stay.isAnonymous = False
        else:
            stay.userName = 'Anonimo'
            stay.isAnonymous = True

        pendingStay.isAuthorize = isAuthorize
        pendingStay.isActive = False
        pendingStay.notifyToUser = True
        stay.save()
        pendingStay.save()
        return Response(status=status.HTTP_200_OK)
      
      
    @api_view(['POST'])    
    def responseUser(request):
        userName = request.data['userName']
        try:
          pendingStay = PendingStay.objects.get(userName=userName, notifyToUser=True)
          pendingStay.notifyToUser = False
          pendingStay.save()
          return Response(status=status.HTTP_200_OK)
        except PendingStay.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND) 
      
    @api_view(['POST'])    
    def createPendingStay(request):
      parking = BicycleParking.objects.get(number=request.data['parkingNumber'])
      place = Place.objects.get(placeNumber=request.data['place'], bicycleParking=parking)
      try:
        associatedStay = Estadia.objects.get(place=place, isActive=True, isAnonymous=True)
        pendingStay = PendingStay.objects.create(userName=request.data['userName'], stay=associatedStay)
        response = {'place': place.placeNumber, 'parking': parking.description}
        return Response(response, status=status.HTTP_200_OK)
      except Estadia.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
      