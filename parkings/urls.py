from django.urls import path
from .views import ParkingsView, BicycleParkingView, EstadiaView

urlpatterns = [
    path('move-create/', ParkingsView.moveCreate, name="move-create"),
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
    
    # path('parkings/<int:pk>/', ParkingsView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]
