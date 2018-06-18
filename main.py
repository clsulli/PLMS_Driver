import time
import pyrebase
import serial
# import qrcode
# import printer
from random import randint

from Lot import LotDetails
from Lot import LotControls
from User import User
from Guest import Guest

guestNum = 1

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

# def printAccountQRCode(data):
#     p = printer.ThermalPrinter()
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_H,
#         box_size=4,
#         border=2,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#
#     img = qr.make_image()
#     img.save("img.bmp")
#
#     from PIL ipmort Image, ImageDraw
#     i = Image.open("img.bmp")
#     data = list(i.getdata())
#     w, h = i.size
#     p.justify("C")
#     p.bold()
#     p.print_text("PLMS\n")
#     p.bold(False)
#     p.bold()
#     p.print_text("Present QR Code to scanner when leaving to pay toll.\n")
#     p.bold(False)
#     p.print_text("Thank you for using PLMS.  Have a nice day!\n\n")
#     p.print_bitmap(data,w,h)
#     p.linefeed(3)


def getSignal(db):

    uid = db.child("qr_code").child("uid").get().val()
    signal = db.child("qr_code").child("signal").get().val()

    return uid, signal


def getSerialSignal():
    #Wait for signal from arduino
    # arduino = serial.Serial('/dev/ttyACM1', 9600)
    # reading = arduino.readline()

    if True:
        guest = Guest("guest%d" % randint(1000, 9999))
        #printAccountQRCode(guest.uid)
        lot1Controls.carEnter(guest, lot1)
        time.sleep(5)
        lot1Controls.carExit(guest, lot1)


firebase, db = setupFirebase()

lot1 = LotDetails(1, 1.25)
lot2 = LotDetails(2, 3.45)
lot3 = LotDetails(3, 2.00)

lot1Controls = LotControls()
lot2Controls = LotControls()
lot3Controls = LotControls()

getSerialSignal()
# while(True):
#
#     getSerialSignal()
#
#     while db.child("qr_code").child("signal").get().val() == "None" or db.child("qr_code").child("uid").get().val() == "None":
#         print(db.child("qr_code").child("signal").get().val())
#
#     print("In function")
#     uid, signal = getSignal(db)
#
#     user = User(uid, "800540630", "clsulli@siue.edu")
#
#     if signal == "Enter":
#         lot1Controls.carEnter(user, lot1)
#         db.child("qr_code").update({"uid": "None"})
#         db.child("qr_code").update({"signal": "None"})
#     elif signal == "Exit":
#         lot1Controls.carExit(user, lot1)
#         db.child("qr_code").update({"uid": "None"})
#         db.child("qr_code").update({"signal": "None"})

# for i in range(0, 60):
#     lot1Controls.updateTime(user)
#     time.sleep(1)
#
# lot1Controls.carExit(user)

# users = db.child("users").get()
# print(users.val())

