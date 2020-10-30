from rest_framework import serializers
from .models import MoveCamera, BicycleParking, Estadia, Segment, Notification
from .models.user import User, BikeOwner
# class ParkingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Parkings
#         fields = ("id", "tl_x", "tl_y", "br_x", "br_y", "isOccupied","patent","cameraId")


class MovesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveCamera
        fields = ("placeNumber", "occupied", "pathPhoto", "createDate")

class BicycleParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BicycleParking
        fields = '__all__'

class EstadiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadia
        fields = '__all__'       

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ("photoPath","datetime","estadia") 

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  
        #fields = ("userName", "photoPath")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  
        #fields = ("name", "email","password")

class BikeOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeOwner
        fields = '__all__'  
        #fields = ("name", "email","password", "bicyclePhoto", "profilePhoto")
