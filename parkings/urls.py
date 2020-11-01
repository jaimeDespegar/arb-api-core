from django.urls import path
from .views import MoveCameraView, BicycleParkingView, EstadiaView, NotificationView, RegisterUserView, NotificationEgressView
from .views import RegisterUserView, CreateUserAPIView, LogoutUserAPIView
from rest_framework.authtoken.views import obtain_auth_token


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
    path('estadias-getUser/<str:pk>/', EstadiaView.getUser, name="estadias-getUser"),
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
    path('bikeOwner-getUser/<str:pk>/', RegisterUserView.registerBikeOwnerGetUser, name="bikeOwner-getUser"),
    path('bikeOwner-update/<int:pk>/', RegisterUserView.registerBikeOwnerUpdate, name="bikeOwner-update"),
    path('bikeOwner-updateUser/<str:pk>/', RegisterUserView.registerBikeOwnerUpdateUser, name="bikeOwner-updateUser"),

    ## Alertas
    path('notificationEgress-get/<int:pk>/', NotificationEgressView.notificationEgressGet, name="notificationEgress-get"),
    path('notificationEgress-getUser/<str:pk>/', NotificationEgressView.notificationEgressGetUser, name="notificationEgress-getUser"),
    path('notificationEgress-getAll/', NotificationEgressView.notificationEgressGetAll, name="notificationEgress-getAll"),
    path('notificationEgress-update/<int:pk>/', NotificationEgressView.notificationEgressUpdate, name="notificationEgress-update"),
    path('notificationEgress-getSuspected/', NotificationEgressView.notificationEgressHistorySuspectedGet, name="notificationEgress-getSuspected"),
    path('notificationEgress-updateUser/<str:pk>/', NotificationEgressView.notificationEgressUpdateUser, name="notificationEgress-updateUser"),
    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('auth/register/', CreateUserAPIView.as_view(), name='auth_user_create'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_user_logout')
    # path('parkings/<int:pk>/', MoveCameraView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]
