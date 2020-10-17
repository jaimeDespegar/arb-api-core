from rest_framework import serializers
from .models import MoveCamera

# class ParkingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Parkings
#         fields = ("id", "tl_x", "tl_y", "br_x", "br_y", "isOccupied","patent","cameraId")


class MovesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveCamera
        fields = ("placeNumber", "occupied", "pathPhoto", "hourGenerated")
