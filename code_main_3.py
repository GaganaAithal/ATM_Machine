import mysql.connector
import re
from twilio.rest import Client
import math, random


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="ATM"
)


mycursor = mydb.cursor()

class ATM:
    def _init_(self, VCN, PHN, PIN):
        self.VCN = VCN
        self.PHN = PHN
        self.PIN = PIN

def menu1():
    print()
    print("\t1.Login")
    print("\t2.Register")
    print("\t3.Exit")
        
def menu2():
    print()
    print("\t1.Withdraw")
    print("\t2.Deposit")
    print("\t3.Transaction history")
    print("\t4.Check balance")
    print("\t5.Change PIN")
    print("\t6.Exit")

def login():
    VCN = int(input("Enter VCN: "))
    limit=5
    if(VCN_match(VCN)):
        while limit > 0:
            login_status=PIN_check()
            if login_status == 1:
                break
            limit=limit-1

    if(login_status):
        while True:
            menu2()
            ch = int(input("\nEnter choice: "))
            if ch==1:
                print("\nWithdraw")
            elif ch==2:
                print("\nDeposit")
            elif ch==3:
                print("\nTransaction History")
            elif ch==4:
                print("\nCheck balance")
            elif ch==5:
                print("\nChange PIN")
            else:
                print("\nThank you for banking with us!")
                break


def validate_re_ph(phone_number):
    # Check if the phone number is in a valid format
    expr = r'^(0|91)?[6-9][0-9]{9}$'
    if not re.match(expr, phone_number):
        print("\nPhone number is invalid")
        return 0

    # Check if the phone number already exists in the database
    mycursor.execute("SELECT COUNT(*) FROM USERS WHERE PHN = %s", (phone_number,))
    result = mycursor.fetchone()
    count = result[0] if result else 0

    if count > 0:
        print("\nAccount with the entered phone number already exists.")
        return 0

    return 1
 


def register():
    ph = input("Enter phone number: ")
    trials = 10
    pin_enter_limit = 3
    PIN=""
    while(trials>0 and (not validate_re_ph(ph))):
        ph = input("\nEnter phone number: ")
        trials=trials-1
    if(trials<=0):
        print("\nTry again later")
        return
   
        

def PIN_check():
    pass

def VCN_match():
    pass

def pin_reset(vcn):
    #set_the_pin(vcn,ph,1)
    pass

while True:
    menu1()
    ch = int(input("\nEnter choice: "))
    if ch == 1:
        login()
    elif ch == 2:
        register()
    else:
        break

