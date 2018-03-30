import pydoc
import time
import pyrebase

from Lot import LotDetails
from Lot import LotControls
from User import User

def setupFirebase():
    config = {
        "apiKey": "AIzaSyDHVz3xeQL7nlB4iNKgH_5aVQxykA5oijE",
        "authDomain": "plmsuserlogin.firebaseapp.com",
        "databaseURL": "https://plmsuserlogin.firebaseio.com/",
        "storageBucket": "none"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return firebase, db

def getUIDFromQRCode():
    return "6HQPugaYw2OnVvpgtRIYqlASNHy2"

firebase, db = setupFirebase()

user = User(getUIDFromQRCode(), "800540630", "clsulli@siue.edu")

lot1 = LotDetails(1, 1.25)
lot2 = LotDetails(2, 3.45)
lot3 = LotDetails(3, 2.00)

lot1Controls = LotControls()
lot2Controls = LotControls()
lot3Controls = LotControls()

lot1Controls.carEnter(user, lot1)

for i in range(0, 60):
    lot1Controls.updateTime(user)
    time.sleep(1)

lot1Controls.carExit(user)

users = db.child("users").get()
print(users.val())

