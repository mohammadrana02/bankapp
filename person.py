class Person:
    def __init__(self, fname, lname, address):
        self.fname = fname
        self.lname = lname
        self.address = address.split()
        self.USER_TYPE = None # to determine which dataframe to edit based on the user (is currently empty)

    def update_first_name(self, fname, df):
        """Updates the user's first name"""
        # updates the name in the csv file
        df.loc[df['fname'] == self.get_first_name(), 'fname'] = fname
        df.to_csv(f'{self.USER_TYPE}.csv', index=False, sep=';')

        old_name = self.get_first_name()

        self.fname = fname # updates the name in the object

        print(f'Old First Name: {old_name}')
        print(f'New First Name: {fname}')

    def update_last_name(self, lname, df):
        """Updates the user's last name"""
        # updates the name in the csv file
        df.loc[df['lname'] == self.get_last_name(), 'lname'] = lname
        df.to_csv(f'{self.USER_TYPE}.csv', index=False, sep=';')

        old_name = self.get_last_name()

        self.lname = lname  # updates the name in the object

        print(f'Old Last Name: {old_name}')
        print(f'New Last Name: {lname}')

    def get_first_name(self):
        """Returns the person's first name"""
        return self.fname

    def get_last_name(self):
        """Returns the person's last name"""
        return self.lname

    def update_address(self, addr, df):
        """Updates the user's address"""
        # updates address in dataframe
        df.loc[df['lname'] == self.get_last_name(), 'address'] = addr
        df.to_csv(f'{self.USER_TYPE}.csv', index=False, sep=';')
        # gets the original address
        old_address = self.get_address()
        # updates address in the customer object
        self.address = addr

        print(f"Old Address: {old_address[0]} {old_address[1]} {old_address[2]}"
              f" {old_address[3]} {old_address[4]} {old_address[5]}")
        print(f'New Address: {addr}')

    def get_address(self):
        """Returns the person's address"""
        return self.address


class Admin(Person):
    def __init__(self, fname, lname, address, user_name, password, full_rights):
        super().__init__(fname, lname, address)
        self.user_name = user_name
        self.password = password
        self.full_admin_rights = full_rights
        self.USER_TYPE = 'admins'

    def set_username(self, uname, df):
        """Updates the admin's username"""
        # changes the username in the dataframe and updates the csv
        df.loc[df['user_name'] == self.get_username(), 'user_name'] = uname
        df.to_csv(f'{self.USER_TYPE}.csv', index=False, sep=';')

        old_uname = self.get_username() # gets the old username

        self.user_name = uname  # changes the username in the object

        print(f'Old Username: {old_uname}')
        print(f'New Username: {uname}')

    def get_username(self):
        """Returns the admin's username"""
        return self.user_name

    def update_password(self, password, df):
        """Updates the admin's password"""
        # changes the password in the dataframe and updates the csv file
        df.loc[df['password'] == self.get_password(), 'password'] = password
        df.to_csv(f'{self.USER_TYPE}.csv', index=False, sep=';')

        # saves the old password before changing it in the object
        old_pass = self.get_password()
        self.password = password

        print(f'Old Password: {old_pass}')
        print(f'New Username: {password}')


    def get_password(self):
        """Returns the admin's password"""
        return self.password

    def set_full_admin_right(self, admin_right):
        """Gives the admin full rights"""
        self.full_admin_rights = admin_right

    def has_full_admin_right(self):
        """Checks if the admin has full rights"""
        return self.full_admin_rights

    def show_details(self):
        """Shows the details of the admin"""
        print("\n Admin Details:")
        print("First name: %s" % self.fname)
        print("Last name: %s" % self.lname)
        print(f"Address: {self.address[0]} {self.address[1]} {self.address[2]}"
              f" {self.address[3]} {self.address[4]} {self.address[5]}")
        print("Username: %s" % self.user_name)
        print("Password: %s" % self.password)
        print("Full Admin Rights? : %s" % self.has_full_admin_right())


    def admin_settings(self):
        """Displays the admin settings and prompts the admin to pick an option"""
        print("1) Set Name")  # change name
        print("2) Set Address")  # change address
        print("3) Set Username")  # change username
        print("4) Set Password")  # change password
        print("5) Show Details") # output all admin details
        print("6) Go back")  # go back to the main menu
        try:
            option = int(input("Choose your option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
        else:
            return option



class CustomerAccount(Person):
    def __init__(self, fname, lname, address, account_no, balance, account_type, interest_rate, overdraft_limit):
        super().__init__(fname, lname, address)
        self.account_no = account_no
        self.balance = float(balance)
        self.account_type = account_type
        self.interest_rate = interest_rate
        self.overdraft_limit = overdraft_limit
        self.USER_TYPE = 'customers'

    def get_account_no(self):
        """Returns the customer's account number"""
        return self.account_no

    def get_balance(self):
        """Returns the customer's balance"""
        return self.balance

    def deposit(self, amount, df):
        """Deposits an amount of money to the user's account"""
        if amount < 0:
            print('Error. Deposit amount less than 0.')
        else:
            df.loc[df['lname'] == self.get_last_name(), 'balance'] += amount
            df.to_csv('customers.csv', index=False, sep=';')
            self.balance += amount

    def withdraw(self, amount, df):
        """Withdraws money out of the user's account"""
        # changes the balance in the dataframe and updates the csv
        df.loc[df['lname'] == self.get_last_name(), 'balance'] -= amount
        df.to_csv('customers.csv', index=False, sep=';')

        # changes the balance in the object
        self.balance -= amount

    def print_balance(self):
        """Displays the user's balance"""
        print(f"\n The account balance is: £{self.balance:.2f}")

    def get_overdraft_limit(self):
        """Returns the user's overdraft name"""
        return self.overdraft_limit

    def account_menu(self):
        """Displays the customer's menu"""
        print("\n Your Transaction Options Are:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1) Deposit money")
        print("2) Withdraw money")
        print("3) Check balance")
        print("4) Update customer name")
        print("5) Update customer address")
        print("6) Show customer details")
        print("7) Back")
        print(" ")
        try:
            option = int(input("Choose your option: "))
        except ValueError:  # catches any non-integer input
            print("Invalid input. Please enter a number.")
        else:
            return option

    def print_details(self):
        """Displays all the customer's details"""
        print("\n Customer Details:")
        print("First name: %s" % self.fname)
        print("Last name: %s" % self.lname)
        print("Account No: %s" % self.account_no)
        print(f"Address: {self.address[0]} {self.address[1]} {self.address[2]}"
              f" {self.address[3]} {self.address[4]} {self.address[5]}")
        print('Balance: %s' % self.balance)
        print('Account Type: %s' % self.account_type)
        print("Interest Rate: %s" % self.interest_rate)
        print("Overdraft Limit: %s" % self.overdraft_limit)


    def run_account_options(self, df):
        """Controls the logic for the customer options"""
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:  # deposit
                old_balance = self.get_balance() # saves old balance to show the user the difference at the end
                while True:
                    try: # asks the user for a deposit amount and checks if it's a number that is greater than 0
                        amount = float(input("\n Please enter amount to be deposited: £"))
                        if amount < 0:
                            print('Error. Deposit amount less than 0.')
                            continue
                    except ValueError:
                        print("Error. Please enter a number.")
                    else:  # deposit amount into customer account and displays old and new balance
                        self.deposit(amount, df)
                        print(f'Old Balance: £{old_balance}')
                        print(f'New Balance: £{self.get_balance()}')
                        break
            elif choice == 2:  # withdraw
                old_balance = self.get_balance()  # saves old balance to show the user the difference at the end
                while True:
                    try:
                        # asks the user for a withdrawal amount and checks if it's a number,
                        # greater than 0 and within the customer's allowance
                        allowance = self.get_balance() + self.overdraft_limit
                        withdraw = float(input("\n Please input the amount to withdraw: £"))
                        if withdraw > allowance:
                            print('Error. Withdrawal amount greater than balance.')
                            continue
                        if withdraw < 0:
                            print('Error. Withdrawal amount less than 0.')
                            continue
                    except ValueError:
                        print("Error. Please enter a number.")
                    else:  # withdraws amount from customers account and displays old and new balance
                        self.withdraw(withdraw, df)
                        print(f'Old Balance: £{old_balance}')
                        print(f'New Balance: £{self.get_balance()}')
                        break

            elif choice == 3:  # print current balance
                print(f'Current Balance: £{self.get_balance()}')

            elif choice == 4:  # update name
                while True:
                    fname = input("\n Enter new customer first name: ")
                    sname = input("\nEnter new customer last name: ")

                    if len(fname) == 0 or len(sname) == 0: # checks if fields are left empty
                        print('Error. Please enter valid names.')
                        continue
                    else: # updates the first and last name
                        self.update_last_name(sname, df)
                        self.update_first_name(fname, df)
                        break

            elif choice == 5:  # update address
                while True:
                    try:  # makes sure that address number is a valid number
                        hnumber = int(input("\nPlease enter the new address number: "))
                    except ValueError:
                        print("Error. Please enter a number.")
                        continue
                    else:  # if address number is valid, then it prompts the user to enter the rest of their address
                        str_name = input("Please enter the new street name: ")
                        city = input("Please enter the new city: ")
                        post_code = input("Please enter the new postcode: ")
                        # formats new address
                        address = f'{hnumber}, {str_name}, {city}, {post_code}'
                        self.update_address(address, df)
                        break
            elif choice == 6:  # displays customer details
                self.print_details()
            elif choice == 7:  # go back to the admin menu
                print("\n Exit account operations")
                break