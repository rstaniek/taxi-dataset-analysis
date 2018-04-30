class TaxiTrip(object):

    def __init__(self, tripID, taxiID, tripStartTImestamp, pickupCommunityArea, lattitude, longitude):
        self.tripID = tripID
        self.taxiID = taxiID
        self.tripStartTimestamp = tripStartTImestamp
        self.pickupCommunityArea = pickupCommunityArea
        self.lattitude = lattitude
        self.longitude = longitude



class CrimeRecord(object):
    def __init__(self, id, date, communityArea, lattitude, longitude):
        self.id = id
        self.date = date
        self.communityArea = communityArea
        self.lattitude = lattitude
        self.longitude = longitude

