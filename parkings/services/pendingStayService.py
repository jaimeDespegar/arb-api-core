from ..daos import PendingStayDao

class PendingStayService:
    
    def __init__(self):
        self.pendingStayDao = PendingStayDao()
    
    def getAll(self):
        return self.pendingStayDao.getAll()
    
    def get(self, filters):
        return self.pendingStayDao.get(filters)

    def filter(self, filters):
        return self.pendingStayDao.filter(filters)
    
    def create(self, newPending):
        self.pendingStayDao.insert(newPending)