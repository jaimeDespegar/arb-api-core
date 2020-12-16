from ..daos import NotificationEgressDao


class NotificationEgressService:
    
    def __init__(self):
        self.notificationEgressDao = NotificationEgressDao()
    
    def create(self, newNotification):
        self.notificationEgressDao.insert(newNotification)
    
    def get(self, filters):
        return self.notificationEgressDao.get(filters)
    
    def getAll(self):
        return self.notificationEgressDao.getAll()