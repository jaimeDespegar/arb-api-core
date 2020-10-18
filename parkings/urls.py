from django.urls import path
from .views import ParkingsView, EstadiaView

urlpatterns = [
    path('move-create/', ParkingsView.moveCreate, name="move-create"),
    
    # Estadia
    path('estadias/', EstadiaView.getAll),
    #path('estadia-detail/<str:user>/', EstadiaView.estadiaDetail, name="estadia-detail"),
    path('estadia-create/', EstadiaView.estadiaCreate, name="estadia-create"),
    path('estadia-update/<int:pk>/', EstadiaView.estadiaUpdate, name="estadia-update"),
    
    # path('parkings/<int:pk>/', ParkingsView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]