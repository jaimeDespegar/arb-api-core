
from ..services.bicycleParkingService import BicycleParkingService

def test_answer():
    b = BicycleParkingService()
    places = b.getCountFreePlaces()
    assert places == 1
