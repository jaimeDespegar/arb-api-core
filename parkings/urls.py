from django.urls import path
from .views import ParkingsView

urlpatterns = [
    path('move-create/', ParkingsView.moveCreate, name="move-create")
    # path('parkings/', ParkingsView.parkings_list),
    # path('parkings/<int:pk>/', ParkingsView.parking_detail),
    # path('configuration/', ConfigurationView.configuration_list),
    # path('configuration/<str:pk>/', ConfigurationView.configuration_detail)
]