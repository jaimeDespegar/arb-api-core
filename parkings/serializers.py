
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import MoveCamera, BicycleParking, Estadia, Segment, NotificationEgress, PendingStay, Place, Configuration
from .models.user import User, BikeOwner


class MovesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveCamera
        fields = ("placeNumber", "occupied", "pathPhoto", "createDate", "photoInBase64")

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
        fields = ("photoPath","dateCreated","estadia") 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  

class BikeOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeOwner
        fields = '__all__'  

class NotificationEgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEgress
        fields = '__all__'  

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class PendingStaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingStay
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        
class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'