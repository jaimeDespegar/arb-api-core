from django.contrib import admin
from .models import Segment, BicycleParking, Notification, Place, Estadia, MoveCamera

# Register your models here.

admin.site.register(Segment)
admin.site.register(BicycleParking)
admin.site.register(Notification)
admin.site.register(Place)
admin.site.register(Estadia)
admin.site.register(MoveCamera)
