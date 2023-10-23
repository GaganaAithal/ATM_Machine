class ATM:
    def __init__(self):
        self.vcn = None
        self.pin = None
        self.balance = 0.0

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Log In with VCN and PIN")
            print("2. Create New Account")
            print("3. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.login()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def login(self):
        # Implement authentication logic here
        pass

    def create_account(self):
        # Implement new account creation logic here
        pass

    def deposit(self):
        # Implement deposit logic here
        pass

    def withdraw(self):
        # Implement withdrawal logic here
        pass

    def check_balance(self):
        # Implement balance check logic here
        pass

    def view_transaction_history(self):
        # Implement transaction history logic here
        pass

    def reset_pin(self):
        # Implement PIN reset logic here
        pass

    def send_otp(self, mobile_number):
        # Implement OTP sending logic here
        pass

    def send_message(self, mobile_number, message):
        # Implement message sending logic here
        pass

    def update_database(self):
        # Implement database update logic here
        pass


if __name__ == "__main__":
    atm = ATM()
    atm.main_menu()
