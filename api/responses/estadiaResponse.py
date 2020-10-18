
class EstadiaResponse():

    def __init__(self, userName, arrival, departure, placeUsed):
        self.userName = userName
        self.arrival = arrival
        self.departures = departure
        self.placeUsed = placeUsed


class SegmentResponse():

    def __init__(self, date, photo):
        self.date = date
        self.photo = photo