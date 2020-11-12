from django.contrib import admin
from .models import Segment, BicycleParking, Notification, Place, Estadia, MoveCamera, NotificationEgress
from .models import BikeOwner, PendingStay

# Register your models here.

admin.site.register(Segment)
admin.site.register(BicycleParking)
admin.site.register(Notification)
admin.site.register(NotificationEgress)
admin.site.register(Place)
admin.site.register(Estadia)
admin.site.register(MoveCamera)
admin.site.register(BikeOwner)
admin.site.register(PendingStay)