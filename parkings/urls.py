from django.urls import path
from .views import MoveCameraView, BicycleParkingView, EstadiaView, NotificationView, RegisterUserView

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
    path('estadias-getAll/', EstadiaView.getAll, name="estadias-getAll"),
    path('estadias-get/<int:pk>/', EstadiaView.get, name="estadias-get"),
    #path('estadia-detail/<str:user>/', EstadiaView.estadiaDetail, name="estadia-detail"),
    path('estadia-create/', EstadiaView.estadiaCreate, name="estadia-create"),
    path('estadia-update/<int:pk>/', EstadiaView.estadiaUpdate, name="estadia-update"),
    path('estadia/find', EstadiaView.findEstadias, name="estadia-find"),    
    
    # Casos sospechosos de robo
    ##path('move-suspected-create/', MoveCameraView.checkSuspectedMove, name="move-suspected-create"),
    path('move-notification-create/', NotificationView.notificationMoveCreate, name="move-notification-create"),
    path('move-notification-get/<int:pk>/', NotificationView.notificationGet, name="move-notification-get"),

    # # Registros de Usuarios
    # path('user-create/', RegisterUserView.registerUserCreate, name="user-create"),
    # path('user-getAll/', RegisterUserView.registerUserGetAll, name="user-getAll"),
    # path('user-get/<int:pk>/', RegisterUserView.registerUserGet, name="user-get"),
    # Registros de Usuarios
    path('bikeOwner-create/', RegisterUserView.registerBikeOwnerCreate, name="bikeOwner-create"),
    path('bikeOwner-getAll/', RegisterUserView.registerBikeOwnerGetAll, name="bikeOwner-getAll"),
    path('bikeOwner-get/<int:pk>/', RegisterUserView.registerBikeOwnerGet, name="bikeOwner-get"),
    path('bikeOwner-update/<int:pk>/', RegisterUserView.registerBikeOwnerUpdate, name="bikeOwner-update"),



    # path('parkings/<int:pk>/', MoveCameraView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]
