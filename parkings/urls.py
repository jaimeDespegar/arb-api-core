from django.urls import path
from .views import ParkingsView
from .views import BicycleParkingView

urlpatterns = [
    path('move-create/', ParkingsView.moveCreate, name="move-create"),
    path('bicycleParking-create/', BicycleParkingView.bicycleParkingCreate, name="bicycleParking-create"),
    path('bicycleParking-getAll/', BicycleParkingView.bicycleParkingGetAll, name="bicycleParking-getAll"),
    path('bicycleParking-get/<int:pk>/', BicycleParkingView.bicycleParkingGet, name="bicycleParking-get")
    
    # path('parkings/', ParkingsView.parkings_list),
    # path('parkings/<int:pk>/', ParkingsView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]