from ..models import Segment


class SegmentDao:
    
    def insert(self, newSegment):
        Segment.objects.create(**newSegment)
    
    def findByFilters(self, filters):
        return Segment.objects.filter(**filters)