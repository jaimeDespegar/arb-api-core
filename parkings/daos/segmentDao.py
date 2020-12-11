from ..models import Segment


class SegmentDao:
    
    def insert(self, newSegment):
        Segment.objects.create(**newSegment)
    
    def findByFilters(self, filters):
        return Segment.objects.filter(**filters)
    
    def get(self, filters):
        try:
            return Segment.objects.get(**filters)
        except Segment.DoesNotExist:
            return None