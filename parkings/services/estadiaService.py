from ..models import Estadia, Segment
from ...api.responses.estadiaResponse import EstadiaResponse, SegmentResponse

class EstadiaService():

    def findByUser(self, userName):
        # TODO
        return []


    def findByRangeDate(self, fromDate, toDate):
        responses = []
        estadias = Estadia.objects.filter(dateCreated__lte=toDate, dateCreated__gte=fromDate)

        for est in estadias:
            segments = Segment.objects.filter(estadia=est)
            for segment in segments: 
                arrival = None
                departure = None
                if segment.segmentType == 'LLEGADA':
                    arrival = SegmentResponse(segment.datetime, segment.photoPath)
                else:
                    departure = SegmentResponse(segment.datetime, segment.photoPath) 

            e = EstadiaResponse('Test', arrival, departure, est.placeUsed)
            responses.append(e)
        
        return responses


    def findAnonymous(self):
        # TODO
        return []
