from ..models import BikeOwner
from django.contrib.auth.models import User


class UserDao:
    
    def getBikeOwner(self, filters):
        return BikeOwner.objects.get(**filters)
    
    def getUser(self, filters):
        return User.objects.get(**filters)
        