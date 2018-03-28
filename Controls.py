from datetime import datetime

class LotControls:
    """
    LotControls encapsulates various functions to simulate parking lot activity that would be seen in day to day
    function of the PLMS application.
    """

    def carEnter(self, user, lot):
        """
        Simulates a car entering the parking lot and performs actions on the User and Lot objects.

        :param user: Reference to the user stored in Google Firebase that entered the parking lot.
        :param lot: Reference to the Lot that the user entered.
        :return: returns nothing.
        """

        cUser = user
        cUser.updateLot(lot)

        cUser.lot.startStamp = str(datetime.now())

    def carExit(self, user):
        """
        Simulates a car exiting the parking lot and performs actions on the User and Lot objects.

        :param user: Reference to the user stored in Google Firebase that exited the parking lot.
        :param lot: Reference to the Lot that the user entered.
        :return: returns nothing.
        """

        cUser = user
        cUser.lot.stopStamp = str(datetime.now())

    def setTotal(self, user):
        """
        Gets total that is due from time spent at lot.

        :param user: Reference to the user that used the lot.
        :return: returns nothing
        """

        cUser = user
        start = cUser.lot.startStamp
        stop = cUser.lot.stopStamp

        elapsedTime = stop - start
        totalMinSec = divmod(elapsedTime)
        

