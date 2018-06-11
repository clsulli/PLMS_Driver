def createGuest(id):
    guestId = "guest%d" % id
    guest = Guest(guestId)

class Guest(object):

    def __init__(self, uid, lot=None):
        self.uid = uid
        self.lot = lot

    def updateLot(self, lot):
        self.lot = lot