class LotDetails:
    """
    LotDetails encapsulates a Lot ID, Lot price for the Lot ID, the Start time of when they entered the lot, the Stop time
    that they exited the lot and the Total due for the time the user used at the parking lot.
    """

    def __init__(self, lotID, lotPrice, startStamp, stopStamp):
        """
        Constructs a new "LOT" Object.

        :param lotID: ID of the lot that is being used.
        :param lotPrice: Price of the lot being used.
        :param startStamp: Time that user entered the lot.
        :param stopStamp: Time that user exited the lot.
        """

        self.lotID = lotID
        self.lotPrice = lotPrice
        self.startStamp = startStamp
        self.stopStamp = stopStamp
