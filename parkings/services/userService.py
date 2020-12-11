from ..daos import UserDao


class UserService:    
    
    def __init__(self):
        self.userDao = UserDao()
    
    def getBikeOwner(self, filters):
        return self.userDao.getBikeOwner(filters)

    def getUser(self, filters):
        return self.userDao.getUser(filters)