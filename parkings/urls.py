from django.urls import path
from .views import MoveCameraView, BicycleParkingView, EstadiaView, RegisterUserView, NotificationEgressView
from .views import RegisterUserView, CreateUserAPIView, LogoutUserAPIView, RecoveryUserView, PendingStayView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('move-create/', MoveCameraView.moveCreate, name="move-create"),
    path('bicycleParking-create/', BicycleParkingView.bicycleParkingCreate, name="bicycleParking-create"),
    path('bicycleParking-get/<int:pk>/', BicycleParkingView.getBicycleParking, name="bicycleParking-get"),
    path('bicycleParking-availability/', BicycleParkingView.bicycleParkingAvailability, name="bicycleParkingAvailability"),
    path('bicycleParking-update/', BicycleParkingView.updateBicicleParking, name="bicycleParking-update"),
    path('bicycleParking-delete/<int:number>/', BicycleParkingView.bicicleParkingDelete, name="bicycleParking-delete"),
    path('bicycleParkingAndPlaces/', BicycleParkingView.getAllBicyclesParkings, name="bicycleParkingAndPlaces"),
    path('movebicycleparking-create/', MoveCameraView.moveBicycleparkingCreate, name="movebicycleparking-create"),
    path('moveplace-create/', MoveCameraView.movePlaceCreate, name="moveplace-create"),



    # Estadia
    path('estadias-getAll/', EstadiaView.getAll, name="estadias-getAll"),
    path('estadias', EstadiaView.find, name="estadias-find"),
    path('estadia/find', EstadiaView.findEstadias, name="estadia-find"),   # renombrar
    path('estadia-getStateBike/<str:pk>/', EstadiaView.getStateBike, name="estadia-getStateBike"), 
    path('parking/entrance/', EstadiaView.createStayEntrance, name='parking-entrance'),
    path('parking/egress/', EstadiaView.createStayEgress, name='parking-egress'),    
    path('estadia/reports/', EstadiaView.findEstadiasReportes, name='estadia-reports'), 
    path('estadia/status', EstadiaView.getStatusStayByUser, name='estadia-status'),     
    path('estadia/pendings', PendingStayView.getPendingsStays, name='parking-pendings'),   
    path('estadia/pendings/response', PendingStayView.responseUser, name='pendings-response'),
    path('estadia/pendings/create/', PendingStayView.createPendingStay, name='pendings-create'),        
    path('estadia/authorize', PendingStayView.authorize, name='parking-authorize'),
    path('estadia/reportsWeek/<int:pk_days>/', EstadiaView.findEstadiasReportesSemanal, name='estadia-reportsWeek'),
    path('estadia/reportsRange/<int:pk>/', EstadiaView.findEstadiasReportesRango, name='estadia-reportsRange'),     
    path('estadia/reportsHourUserWeek/<str:pk>/<int:pk_days>/', EstadiaView.findHourUserEstadiaWeekReportes, name='estadia-reportsHourUserWeek'),  
    path('estadia/reportsHourAllWeek/<int:pk_days>/', EstadiaView.findHourAllEstadiaWeekReportes, name='estadia-reportsHourAllWeek'),  
    path('estadia/reportsPromedioHourUserWeek/', EstadiaView.findPromedioHourUserEstadiaWeekReportes, name='estadia-reportsPromedioHourUserWeek'),  
    path('estadia/reportsHourAllSuspectedAndPeakTime/<int:pk_days>/', EstadiaView.findHourAllSuspectedAndPeakTime, name='estadia-reportsHourAllSuspectedAndPeakTime'),   
    path('estadia/cleanOldStadias/', EstadiaView.cleanOldStadias, name='estadia-cleanOldStadias'),   


    # Registros de Usuarios
    path('bikeOwner-create/', RegisterUserView.registerBikeOwnerCreate, name="bikeOwner-create"),
    path('bikeOwner-getAll/', RegisterUserView.registerBikeOwnerGetAll, name="bikeOwner-getAll"),
    path('bikeOwner-get/<int:pk>/', RegisterUserView.registerBikeOwnerGet, name="bikeOwner-get"),
    path('bikeOwner-getUser/<str:pk>/', RegisterUserView.registerBikeOwnerGetUser, name="bikeOwner-getUser"),
    path('bikeOwner/update/<str:pk>/', RegisterUserView.registerBikeOwnerUpdateUser, name="bikeOwner-updateUser"),
    path('bikeOwner-delete/<str:pk>/', RegisterUserView.bikeOwnerDelete, name="bikeOwner-delete"),
    path('bikeOwnerParser-getAll/', RegisterUserView.parseBikeOwnerGetAll, name="bikeOwnerParser-getAll"),
    path('bikeOwnerParser-Find', RegisterUserView.parseBikeOwnerFind, name="bikeOwnerParser-Find"),
    
    ## Alertas
    path('notificationEgress-getUser/<str:pk>/', NotificationEgressView.notificationEgressGetUser, name="notificationEgress-getUser"),
    path('notificationEgress-getAll/', NotificationEgressView.notificationEgressGetAll, name="notificationEgress-getAll"),
    path('notificationEgress-update/<str:pk>/', NotificationEgressView.notificationEgressUpdateUser, name="notificationEgress-updateUser"),

    # Registros de Usuarios
    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('auth/register/', CreateUserAPIView.as_view(), name='auth_user_create'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_user_logout'),
    path('bikeOwner/recovery/<str:pk>/', RecoveryUserView.recoveryBikeOwnerUpdateUser, name='bikeOwner_recovery'),


    # Recuperar contraseña en django 2.1 
    #path('reset/password_reset',auth_views.PasswordResetView.as_view(),name='password_reset_form'),
    ##path('reset/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html'), name="password_reset"),
    #path('reset/password_reset/', csrf_exempt(auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html')), name="password_reset"),
    ##path('reset/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    ##path('reset/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    ##path('reset/password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
                

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]


