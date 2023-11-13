import mysql.connector
import re
from twilio.rest import Client
import math, random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sivam@123",
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
    limit = 4
    if VCN_match(VCN):
        while limit > 0:
            if PIN_check(VCN):
                break
            else:
                print(f"Incorrect PIN. {limit - 1} attempts remaining.")
            limit -= 1
        if limit == 0:
            print("Maximum PIN attempts reached. Exiting.")
            return
    else:
        print("VCN not found. Exiting.")
        return

    while True:
        menu2()
        ch = int(input("\nEnter choice: "))
        if ch == 1:
            print("\nWithdraw")
        elif ch == 2:
            print("\nDeposit")
        elif ch == 3:
            print("\nTransaction History")
        elif ch == 4:
            print("\nCheck balance")
        elif ch == 5:
            # Call the set_the_pin function to change the PIN
            set_the_pin(VCN, None, 1)
        else:
            print("\nThank you for banking with us!")
            break


def validate_re_ph(phone_number):
    expr = r'^(0|91)?[6-9][0-9]{9}$'
    if not re.match(expr, phone_number):
        print("\nPhone number is invalid")
        return 0

    mycursor.execute("SELECT COUNT(*) FROM USERS WHERE PHN = %s", (phone_number,))
    result = mycursor.fetchone()
    count = result[0] if result else 0

    if count > 0:
        print("\nAccount with the entered phone number already exists.")
        return 0

    return 1

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_verify_otp(ph, VCN_exist):
    otp = generateOTP()
    if not VCN_exist:
        limit_otp_send = 5

    ask_user = 1

    while limit_otp_send > 0 and ask_user:
        limit_otp_match = 5
        if len(ph) == 10:
            ph = "+91" + ph
        #account_sid = 'removed for privacy purpose'
        #auth_token = 'removed for privacy purpose'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            #from_='+14242964617',
            body='ATM simulator OTP: ' + otp,
            to=ph
        )
        print("\nOTP sent to your mobile number")
        input_otp = input("\nEnter OTP sent:")

        while input_otp != otp and limit_otp_match > 1:
            input_otp = input("\nRe-enter OTP sent: ")
            limit_otp_match = limit_otp_match - 1

        if limit_otp_match <= 1:
            print("\t1.Resend OTP")
            print("\t2. Later")
            ask_user = int(input("Select an option "))
            if ask_user == 1:
                pass
            elif ask_user == 2:
                ask_user = 0
                if VCN_exist:
                    limit_left = limit_otp_send
            else:
                print("\t1.Enter a valid option")
        else:
            print("\nOTP successfully verified!")
            return 1
        limit_otp_send = limit_otp_send - 1

    if limit_otp_send <= 0:
        print("\tTry again later after 24 hours")
    elif ask_user == 0:
        print("\tTry again later")

    return 0

def set_the_pin(vcn, ph, vcn_exist):
    temp_limit = 3

    input_PIN = input("\nEnter a 4 digit PIN:")

    if len(input_PIN) == 4 and input_PIN.isdigit():
        while temp_limit > 0:
            c_input_PIN = input("\nRe-enter PIN to confirm:")
            if c_input_PIN != input_PIN:
                print("\nThe PINs do not match")
                temp_limit = temp_limit - 1
            else:
                if vcn_exist == 0:  # Check if it's a new registration
                    sql = "insert into USERS (VCN, PHN, PIN) values(%s, %s, %s)"
                    val = (vcn, ph, c_input_PIN)
                else:  # It's a PIN change, update the existing record
                    sql = "UPDATE USERS SET PIN = %s WHERE VCN = %s"
                    val = (c_input_PIN, vcn)
                mycursor.execute(sql, val)
                mydb.commit()
                print("\nYou've successfully set your PIN")
                return 3
    else:
        print("\nEnter a valid PIN")
        return 2
    return 1



def register():
    ph = input("Enter phone number: ")
    trials = 10
    pin_enter_limit = 3
    PIN = ""
    while trials > 0 and (not validate_re_ph(ph)):
        ph = input("\nEnter phone number: ")
        trials = trials - 1
    if trials <= 0:
        print("\nTry again later")
        return
    try:
        if send_verify_otp(ph, 0):
            mycursor.execute("SELECT VCN FROM USERS ORDER BY VCN DESC LIMIT 1")
            result = mycursor.fetchone()
            y = 0
            if result is not None:
                y = result[0]
            vcn = y + 1
            print("\nYou can set the PIN now!")
            VCN_PIN_status = set_the_pin(vcn, ph, 0)
            ask_user = 1
            while (ask_user == 1) and (VCN_PIN_status == 1 or VCN_PIN_status == 2) and pin_enter_limit > 1:
                print("\n\t1.Set PIN")
                print("\t2.Exit")
                ask_user = int(input("\nSelect an option "))
                if ask_user == 1:
                    VCN_PIN_status = set_the_pin(vcn, ph, 0)
                    pin_enter_limit = pin_enter_limit - 1
                elif ask_user == 2:
                    print("\nPlease try again later")
                else:
                    print("\nPlease enter a valid option")
            if pin_enter_limit == 1:
                print("\nAccount registration unsuccessful. Please try again later")
    except Exception as e:
        if "send_verify_otp" in str(e):
            print("\nPhone number is not verified by Twilio (dev stage)")
def PIN_check(VCN):
    entered_PIN = input("Enter the PIN: ")
    mycursor.execute("SELECT PIN FROM USERS WHERE VCN = %s", (VCN,))
    result = mycursor.fetchone()
    if result:
        stored_PIN = result[0]
        if entered_PIN == stored_PIN:
            return True
    return False

def VCN_match(VCN):
    mycursor.execute("SELECT COUNT(*) FROM USERS WHERE VCN = %s", (VCN,))
    result = mycursor.fetchone()
    count = result[0] if result else 0
    if count > 0:
        return True
    return False

def pin_reset(VCN):
    if VCN_match(VCN):
        ph = input("Enter your phone number: ")
        if validate_re_ph(ph):
            if send_verify_otp(ph, 1):
                new_pin = input("Enter a new 4-digit PIN: ")
                if len(new_pin) == 4 and new_pin.isdigit():
                    c_new_pin = input("Re-enter the new PIN to confirm: ")
                    if new_pin == c_new_pin:
                        mycursor.execute("UPDATE USERS SET PIN = %s WHERE VCN = %s", (new_pin, VCN))
                        mydb.commit()
                        print("PIN reset successful")
                    else:
                        print("The new PINs do not match. PIN reset failed")
                else:
                    print("Enter a valid 4-digit PIN")
            else:
                print("OTP verification failed. PIN reset failed")
        else:
            print("Invalid phone number. PIN reset failed")
    else:
        print("VCN not found. PIN reset failed")

while True:
    menu1()
    ch = int(input("\nEnter choice: "))
    if ch == 1:
        login()
    elif ch == 2:
        register()
    
    else:
        break
this is the whole code
