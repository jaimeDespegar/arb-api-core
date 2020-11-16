from django.urls import path
from .views import MoveCameraView, BicycleParkingView, EstadiaView, NotificationView, RegisterUserView, NotificationEgressView
from .views import RegisterUserView, CreateUserAPIView, LogoutUserAPIView, RecoveryUserView, PendingStayView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('move-create/', MoveCameraView.moveCreate, name="move-create"),
    path('bicycleParking-create/', BicycleParkingView.bicycleParkingCreate, name="bicycleParking-create"),
    path('bicycleParking-get/<int:pk>/', BicycleParkingView.getBicycleParking, name="bicycleParking-get"),
    path('bicycleParking-availability/', BicycleParkingView.bicycleParkingAvailability, name="bicycleParkingAvailability"),
    path('bicycleParking-update/', BicycleParkingView.updateBicicleParking, name="bicycleParking-update"),
    path('bicycleParking-delete/<int:number>/', BicycleParkingView.bicicleParkingDelete, name="bicycleParking-delete"),
    path('bicycleParkingAndPlaces/', BicycleParkingView.getAllBicyclesParkings, name="bicycleParkingAndPlaces"),

    # Estadia
    path('estadias-getAll/', EstadiaView.getAll, name="estadias-getAll"),
    path('estadias', EstadiaView.find, name="estadias-find"),
    #path('estadia-update/<int:pk>/', EstadiaView.estadiaUpdate, name="estadia-update"),
    path('estadia/find', EstadiaView.findEstadias, name="estadia-find"),   # renombrar
    path('estadia-getStateBike/<str:pk>/', EstadiaView.getStateBike, name="estadia-getStateBike"), 
    path('parking/entrance/', EstadiaView.createStayEntrance, name='parking-entrance'),
    path('parking/egress/', EstadiaView.createStayEgress, name='parking-egress'),    
    path('estadia/reports/', EstadiaView.findEstadiasReportes, name='estadia-reports'), 
    path('estadia/pendings', PendingStayView.getPendingsStays, name='parking-pendings'),        
    path('estadia/authorize', PendingStayView.authorize, name='parking-authorize'),
    path('estadia/reportsWeek/', EstadiaView.findEstadiasReportesSemanal, name='estadia-reportsWeek'),            

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
    #path('bikeOwner-update/<int:pk>/', RegisterUserView.registerBikeOwnerUpdate, name="bikeOwner-update"),
    path('bikeOwner/update/<str:pk>/', RegisterUserView.registerBikeOwnerUpdateUser, name="bikeOwner-updateUser"),
    path('bikeOwner-delete/<str:pk>/', RegisterUserView.bikeOwnerDelete, name="bikeOwner-delete"),
    path('bikeOwnerParser-getAll/', RegisterUserView.parseBikeOwnerGetAll, name="bikeOwnerParser-getAll"),
    path('bikeOwnerParser-Find', RegisterUserView.parseBikeOwnerFind, name="bikeOwnerParser-Find"),
    

    ## Alertas
    path('notificationEgress-get/<int:pk>/', NotificationEgressView.notificationEgressGet, name="notificationEgress-get"),
    path('notificationEgress-getUser/<str:pk>/', NotificationEgressView.notificationEgressGetUser, name="notificationEgress-getUser"),
    path('notificationEgress-getAll/', NotificationEgressView.notificationEgressGetAll, name="notificationEgress-getAll"),
    #path('notificationEgress-update/<int:pk>/', NotificationEgressView.notificationEgressUpdate, name="notificationEgress-update"),
    path('notificationEgress-getSuspected/', NotificationEgressView.notificationEgressHistorySuspectedGet, name="notificationEgress-getSuspected"),
    path('notificationEgress-update/<str:pk>/', NotificationEgressView.notificationEgressUpdateUser, name="notificationEgress-updateUser"),
    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('auth/register/', CreateUserAPIView.as_view(), name='auth_user_create'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_user_logout'),
    path('bikeOwner/recovery/<str:pk>/', RecoveryUserView.recoveryBikeOwnerUpdateUser, name='bikeOwner_recovery')


    # path('parkings/<int:pk>/', MoveCameraView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]
