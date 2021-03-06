from django.contrib import admin
from .models import Segment, BicycleParking, Place, Estadia, MoveCamera, NotificationEgress
from .models import BikeOwner, PendingStay, Configuration

# Register your models here.

admin.site.register(Segment)
admin.site.register(BicycleParking)
admin.site.register(NotificationEgress)
admin.site.register(Place)
admin.site.register(Estadia)
admin.site.register(MoveCamera)
admin.site.register(BikeOwner)
admin.site.register(PendingStay)
admin.site.register(Configuration)