class Coordinate(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


    @property
    def point(self):
        return {'x' : self.latitude,
                'y' : self.longitude}


class TaxiTrip(Coordinate):

    def __init__(self, tripID, tripStartTImestamp, pickupCommunityArea, lattitude, longitude):
        self.trip_id = tripID
        self.tripStartTimestamp = tripStartTImestamp
        self.pickupCommunityArea = pickupCommunityArea
        super(TaxiTrip, self).__init__(lattitude, longitude)


class CrimeRecord(Coordinate):
    def __init__(self, id, date, communityArea, lattitude, longitude):
        self.id = id
        self.date = date
        self.community_area = communityArea
        super(CrimeRecord, self).__init__(lattitude, longitude)
