from ..daos import SegmentDao


class SegmentService:
    
    def get(self, filters):
        return SegmentDao().get(filters)