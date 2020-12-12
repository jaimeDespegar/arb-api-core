from ..daos import UserDao


class UserService:    
    
    def __init__(self):
        self.userDao = UserDao()
    
    def getBikeOwner(self, filters):
        return self.userDao.getBikeOwner(filters)
    
    def getBikeOwnerByFilters(self, filters):
        return self.userDao.getBikeOwnerByFilters(filters)    

    def getUser(self, filters):
        return self.userDao.getUser(filters)
    
    def getAllBikeOwner(self):
        return self.userDao.getAllBikeOwner()

    def createBikeOwner(self, newBikeOwner):
        self.userDao.createBikeOwner(newBikeOwner)