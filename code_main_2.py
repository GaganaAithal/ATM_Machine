class ATM:
    def __init__(self, VCN, PHN, PIN):
        self.VIC = VCN
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


def register():
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









        
