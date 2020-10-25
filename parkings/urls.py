from django.urls import path
from .views import MoveCameraView, BicycleParkingView, EstadiaView, NotificationView

urlpatterns = [
    path('move-create/', MoveCameraView.moveCreate, name="move-create"),
    path('bicycleParking-create/', BicycleParkingView.bicycleParkingCreate, name="bicycleParking-create"),
    path('bicycleParking-getAll/', BicycleParkingView.bicycleParkingGetAll, name="bicycleParking-getAll"),
    path('bicycleParking-get/<int:pk>/', BicycleParkingView.bicycleParkingGet, name="bicycleParking-get"),
    path('bicycleParking-availability/', BicycleParkingView.bicycleParkingAvailability, name="bicycleParkingAvailability"),
    path('bicycleParking-update/<int:pk>/', BicycleParkingView.bicicleParkingUpdate, name="bicycleParking-update"),
    path('bicycleParking-delete/<int:pk>/', BicycleParkingView.bicicleParkingDelete, name="bicycleParking-delete"),
    path('bicycleParkingAndPlaces/', BicycleParkingView.bicycleParkingAndPlacesGetAll, name="bicycleParkingAndPlaces"),

    # Estadia
    path('estadias/', EstadiaView.getAll),
    #path('estadia-detail/<str:user>/', EstadiaView.estadiaDetail, name="estadia-detail"),
    path('estadia-create/', EstadiaView.estadiaCreate, name="estadia-create"),
    path('estadia-update/<int:pk>/', EstadiaView.estadiaUpdate, name="estadia-update"),
    
    # Casos sospechosos de robo
    path('move-suspected-create/', MoveCameraView.checkSuspectedMove, name="move-suspected-create"),
    path('move-notification-create/', NotificationView.notificationMoveCreate, name="move-notification-create"),
    path('move-notification-get/<int:pk>/', NotificationView.notificationGet, name="move-notification-get"),

    # path('parkings/<int:pk>/', MoveCameraView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]
