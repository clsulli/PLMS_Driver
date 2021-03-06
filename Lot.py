from datetime import datetime
import pyrebase
from User import User
from Guest import Guest
import serial
import time

def setupFirebase():
    config = {
        "apiKey": "AIzaSyDHVz3xeQL7nlB4iNKgH_5aVQxykA5oijE",
        "authDomain": "plmsuserlogin.firebaseapp.com",
        "databaseURL": "https://plmsuserlogin.firebaseio.com/",
        "storageBucket": "none"
    }

    return pyrebase.initialize_app(config)

class LotDetails:
    """
    LotDetails encapsulates a Lot ID, Lot price for the Lot ID, the Start time of when they entered the lot, the Stop time
    that they exited the lot and the Total due for the time the user used at the parking lot.
    """

    def __init__(self, lotID, lotPrice, startStamp=None, stopStamp=None, totalDue=None):
        """
        Constructs a new "LOT" Object.

        :param lotID: ID of the lot that is being used.
        :param lotPrice: Price of the lot being used.
        :param startStamp: Time that user entered the lot.
        :param stopStamp: Time that user exited the lot.
        :param totalDue: Total amount due for stay at lot.
        """

        self.lotID = lotID
        self.lotPrice = lotPrice
        self.startStamp = startStamp
        self.stopStamp = stopStamp
        self.totalDue = totalDue

class LotControls:
    """
    LotControls encapsulates various functions to simulate parking lot activity that would be seen in day to day
    function of the PLMS application.
    """

    firebase = setupFirebase()
    db = firebase.database()
    currTotal = 0

    def getDBPath(self, user):
        if type(user) is User:
            DB_PATH = "users"
        elif type(user) is Guest:
            DB_PATH = "guestUsers"

        return DB_PATH

    def carEnter(self, user, lot, dbRef= db):
        """
        Simulates a car entering the parking lot and performs actions on the User and Lot objects.

        :param user: Reference to the user stored in Google Firebase that entered the parking lot.
        :param lot: Reference to the Lot that the user entered.
        :param dbRef: Reference to the Firebase database
        :return: returns nothing.
        """

        DB_PATH = self.getDBPath(user)

        cUser = user
        cUser.updateLot(lot)

        cUser.lot.startStamp = datetime.now()
        dbRef.child(DB_PATH).child(user.uid).update({"startStamp": str(cUser.lot.startStamp)})
        self.incLot(cUser.lot.lotID, self.currTotal)

    def carExit(self, user, lot, dbRef= db):
        """
        Simulates a car exiting the parking lot and performs actions on the User and Lot objects.

        :param user: Reference to the user stored in Google Firebase that exited the parking lot.
        :param lot: Reference to the Lot that the user entered.
        :param dbRef: Reference to the Firebase database
        :return: returns nothing.
        """

        DB_PATH = self.getDBPath(user)

        cUser = user
        cUser.updateLot(lot)
        cUser.lot.startStamp = datetime.strptime(dbRef.child(DB_PATH).child(cUser.uid).child("startStamp").get().val(), "%Y-%m-%d %H:%M:%S.%f")
        cUser.lot.stopStamp = datetime.now()
        dbRef.child(DB_PATH).child(cUser.uid).update({"stopStamp": str(cUser.lot.stopStamp)})
        self.setTotal(cUser)
        dbRef.child(DB_PATH).child(cUser.uid).update({"totalDue": cUser.lot.totalDue})
        self.decLot(cUser.lot.lotID, self.currTotal)
        if "guest" in cUser.uid:
            self.guestTotal(cUser.uid)

    def guestTotal(self, guestId, dbRef = db):
        totalDue = dbRef.child("guestUsers").child(guestId).child("totalDue").get().val()
        ser = serial.Serial('/dev/ttyACM1', 9600)
        time.sleep(1)
        ser.write(guestId + "," + totalDue)
        return totalDue

    def updateTime(self, user, dbRef=db):
        """
        Increments time by one and updates total in real time.

        :param user: Reference to the user that is using the lot.
        :param dbRef: Reference to the Firebase database.
        :return: returns nothing.
        """

        DB_PATH = self.getDBPath(user)

        cUser = user
        cUser.lot.stopStamp = datetime.now()
        dbRef.child(DB_PATH).child(cUser.uid).update({"stopStamp": str(cUser.lot.stopStamp)})
        self.setTotal(cUser);
        dbRef.child(DB_PATH).child(cUser.uid).update({"totalDue": cUser.lot.totalDue})

    def setTotal(self, user, dbRef=db):
        """
        Gets total that is due from time spent at lot.

        :param user: Reference to the user that used the lot.
        :param dbRef: Reference to the Firebase database
        :return: returns nothing
        """

        cUser = user
        start = cUser.lot.startStamp
        stop = cUser.lot.stopStamp

        elapsedTime = stop - start
        totalMinSec = divmod(elapsedTime.total_seconds(), 1)
        secsElapsed = totalMinSec[0]

        cUser.lot.totalDue = (user.lot.lotPrice) * (1/60)*secsElapsed
        #print(cUser.lot.totalDue)

        cUser.lot.totalDue = '${:,.2f}'.format(cUser.lot.totalDue)
        #print(cUser.lot.totalDue)

        return cUser.lot.totalDue


    def incLot(self, lotID, currTotal, dbRef= db):
        """
        Increments Lot's capacity of current lot by one

        :param lotID: The Lot that is being used
        :param currTotal: The total that is currently parked in the lot.
        :param dbRef: Reference to the Firebase database
        :return: returns nothing
        """

        dbRef.child("lots").update({"Lot"+str(lotID): str(currTotal+1)+"/25"})
        self.currTotal = self.currTotal + 1

    def decLot(self, lotID, currTotal, dbRef= db):
        """
        Decrements Lot's capacity of current lot by one

        :param lotID: The Lot that is being used
        :param currTotal: The total that is currently parked in the lot
        :param dbRef: Reference to the Firebase database
        :return: returns nothing
        """

        dbRef.child("lots").update({"Lot"+str(lotID): str(currTotal-1)+"/25"})
        self.currTotal = self.currTotal - 1




