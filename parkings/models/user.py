from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return 'User '+  self.name + ', email ' + self.email

class BikeOwner(User):
    bicyclePhoto = models.CharField(max_length=200)
    profilePhoto = models.CharField(max_length=200)


# class Admin(User):

#     def __init__(self, email, password):
#         super().__init__(email, password)
#         self.name = models.CharField(max_length=200)

#     def __str__(self):
#         return 'Admin ' + self.name

# class SecurityPerson(User):

#     def __init__(self, email, password):
#         super().__init__(email, password)
#         name = models.CharField(max_length=200)