from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services import EstadiaService, PendingStayService, BicycleParkingService
from ..services import SegmentService, UserService


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
            
        items = PendingStayService().filter(filters)

        response = []
        segmentService = SegmentService()
        userService = UserService()
        for i in items:
            place=i.stay.place
            entrance = segmentService.get({"estadia__exact":i.stay, "segmentType__exact":'LLEGADA'})
            user = userService.getUser({"username__exact": i.userName})
            bikeOwner = userService.getBikeOwner({"user__exact": user})
            item = {
              'userName': i.userName,
              'dateCreated': i.dateCreated,
              'place': place.placeNumber,
              'isAuthorize': i.isAuthorize,
              'isActive': i.isActive,
              'bicycleParking': {
                'number': place.bicycleParking.number,
                'description': place.bicycleParking.description
              },
              'photos': {
                'user': bikeOwner.profilePhoto,
                'entrance': entrance.photoInBase64
              }
            }
            response.append(item)

        return Response(response)


    @api_view(['POST'])    
    def authorize(request):
        userName = request.data['userName']
        isAuthorize = request.data['isAuthorize']
        
        pendingStay = PendingStayService().get({"userName__exact":userName, "isActive__exact":True})
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
      
      pendingStay = PendingStayService().get({"userName__exact":userName, "notifyToUser__exact":True})
      if (pendingStay is not None):
        pendingStay.notifyToUser = False
        pendingStay.save()
        return Response(status=status.HTTP_200_OK)
      else:
        return Response(status=status.HTTP_404_NOT_FOUND) 
      
    @api_view(['POST'])    
    def createPendingStay(request):
      service = BicycleParkingService()
      parking = service.get({"number__exact": request.data['parkingNumber']})
      place = service.getPlace({"placeNumber__exact": request.data['place'], "bicycleParking__exact": parking})
      
      associatedStay = EstadiaService().get({"place__exact": place, 
                                             "isActive__exact": True, 
                                             "isAnonymous__exact": True})
      if (associatedStay is not None):
        pendingStay = PendingStayService().create({ "userName": request.data['userName'],
                                                    "stay": associatedStay})
        response = {'place': place.placeNumber, 'parking': parking.description}
        return Response(response, status=status.HTTP_200_OK)
      else:
        return Response(status=status.HTTP_404_NOT_FOUND)
      