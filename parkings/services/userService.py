from django.contrib.auth.models import User


class UserService():
    
    
    def createUser():
        # Create user and save to the database
        user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

        # Update fields and then save again
        user.first_name = 'John'
        user.last_name = 'Test'
        user.save()
    

    def updateUser():
        userToEdit = User.objects.get(email='test')
        userToEdit.first_name=''
        userToEdit.password=''
        userToEdit.email=''
        
        userToEdit.save()
        
        