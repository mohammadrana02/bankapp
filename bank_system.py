from person import * #import person, customer and admin classes
import pandas as pd # pandas used for managing the customer data in the csv file
pd.set_option('display.max_columns', None) # so the user's data won't be truncated when it is printed to the console

class BankSystem(object):

	def __init__(self):
		self.customer = None
		self.admin = None
		self.load_bank_data()

	def load_bank_data(self):
		"""Loads the customer and admin data into respective dataframes"""

		try:  # attempts to load the customer data (stores in a csv) into a dataframe while checking for exceptions
			self.customer = pd.read_csv('customers.csv', sep=';')
		except FileNotFoundError:
			print("Error: 'customers.csv' not found. Please check the file path.")
			self.customer = pd.DataFrame()  # empty dataframe to avoid a future crash
		except pd.errors.ParserError:
			print("Error: 'customers.csv' is corrupted or improperly formatted.")

		try:  # attempts to load the admin data (stores in a csv) into a dataframe while checking for exceptions
			self.admin = pd.read_csv('admins.csv', sep=';')
		except FileNotFoundError:
			print("Error: 'admins.csv' not found. Please check the file path.")
			self.admin = pd.DataFrame()  # empty dataframe to avoid a future crash
		except pd.errors.ParserError:
			print("Error: 'admins.csv' is corrupted or improperly formatted.")

	def admin_login(self, username, password):
		"""Checks if the username and password details are correct for the admin"""
		found_admin = self.search_admins_by_name(username) # first searches for the admin based on username
		msg = "\n Login failed"
		if found_admin is not None: # if the admin is found, it checks if the password is correct
			if str(found_admin.get_password()) == password:
				msg = "\n Login successful"

		return msg, found_admin



	def search_admins_by_name(self, admin_username):
		"""searches for admin based on a given username"""
		# checks the usernames in the admin dataframe
		user_exists = self.admin[self.admin['user_name'] == admin_username]
		if not user_exists.empty:
			# if the account number is a match. get the first matching row (if any)
			user_data = user_exists.iloc[0]

			# creating the admin object using the matching fields in the dataframe
			admin_obj = Admin(
				fname=user_data['fname'],
				lname=user_data['lname'],
				address=user_data['address'],
				user_name=user_data['user_name'],
				password=user_data['password'],
				full_rights=user_data['full_rights'])

			# a customer object is created or an error message depending on whether a match was found
			return admin_obj
		else:
			print("\n The Admin %s does not exist! Try again...\n" % admin_username)


	def search_customers_by_name(self, lname):
		"""searches for customers by their last name and returns a customer object if found"""

		# checks the last names in the customers dataframe
		user_exists = self.customer[(self.customer['lname'] == lname)]

		if not user_exists.empty:
			# if the account number is a match. get the first matching row (if any)
			user_data = user_exists.iloc[0]

			# creating the customer object using the matching fields in the dataframe
			cust_obj = CustomerAccount(
				fname=user_data['fname'],
				lname=user_data['lname'],
				address=user_data['address'],
				account_no=user_data['account_no'],
				balance=user_data['balance'],
				account_type=user_data['account_type'],
				interest_rate=user_data['interest_rate'],
				overdraft_limit=user_data['overdraft_limit'])

			# a success message along with a customer object is returned otherwise an error message with no object
			return 'Success. User found.', cust_obj
		else:
			return 'User does not exist.', None

	def main_menu(self):
		"""displays the main menu and prompts the user to either login as admin or quit"""
		print('')
		print('')
		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print ("Welcome to the Python Bank System")
		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print ("1) Admin login")
		print ("2) Quit Python Bank System")
		print (" ")
		try: # catches any non integer values
			option = int(input("Choose your option: "))
		except ValueError:
			print('Error. Please enter a number.')
		else:
			return option

	def run_main_options(self):
		"""Controls how the main_menu options work"""
		loop = 1
		while loop == 1:
			choice = self.main_menu()
			while True:
				if choice == 1:
					# the user is prompted to input their username and password
					username = input("\n Please input admin username: ")
					password = input("\n Please input admin password: ")
					msg, admin_obj = self.admin_login(username, password)
					print(msg)
					# if the login was successful then it displays the admin options
					if admin_obj is not None and msg == "\n Login successful":
						self.run_admin_options(admin_obj)
					else: # otherwise the loop restarts
						continue
				elif choice == 2:
					# closes the app using the quit() function
					loop = 0
					print ("\n Thank you for stopping by the bank!")
					quit()
				else: # if the input was invalid the loop will repeat
					print('Invalid input. Try again.')
					break

	def transferMoney(self, sender_lname, receiver_lname, receiver_account_no, amount):
		"""Transfers money between two customers"""
		# creates a sender and receiver object
		msg, sender = self.search_customers_by_name(sender_lname)
		msg, receiver = self.search_customers_by_name(receiver_lname)

		# checks if the customers were in the dataframe and if the account number matches
		if sender is None: print('Sender was not found.')
		if receiver is None: print('Receiver was not found.')
		if int(receiver_account_no) != int(receiver.get_account_no()):print('Receiver account number does not match.')
		else: # checks if the transfer amount is within the customer's allowance
			allowance = sender.get_balance() + sender.overdraft_limit
			if amount > allowance:
				print('Error. Transfer amount greater than balance.')
			else:
				# withdraws from sender and deposits into receiver account
				sender.withdraw(amount, self.customer)
				receiver.deposit(amount, self.customer)

				# displays the updated balances
				print(f'Sender Balance: £{sender.get_balance()}')
				print(f'Receiver Balance: £{receiver.get_balance()}')


	def admin_menu(self, admin_obj):
		"""Displays the admin menu and prompts the user to make a choice"""
		print (" ")
		print ("Welcome Admin %s %s : Available options are:" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print ("1) Transfer money") # transfer from one account to another
		# deposit, withdraw, view details, check balance, update details, print details
		print ("2) Customer account operations & profile settings")
		print ("3) Delete customer") # delete customer if admin has full right
		print ("4) Print all customers details")
		print("5) Admin settings") # admin can change account details
		print("6) Print management report")
		print ("7) Sign out")
		print (" ")
		try: # catches any input that isn't an integer
			option = int(input("Choose your option: "))
		except ValueError:
			print('Error. Please enter a number.')
		else:
			return option

	def run_admin_options(self, admin_obj):
		"""Controls how the options work for the admin menu"""
		loop = 1
		while loop == 1:
			choice = self.admin_menu(admin_obj) # prompts the user to pick an option from the admin menu
			if choice == 1: # allows the admin to transfer from one account to another
				while True:
					try: # prompts the admin to enter the amount to transfer while checking if the input is a float
						amount = float(input("\n Please input the amount to be transferred: £"))
						if amount < 0: # makes sure the amount is a number that is greater than zero
							print('Error. Transfer amount less than 0.')
							continue
					except ValueError:
						print('Error. Please enter a number.')
					else:
						# prompts user to input sender surname, receive surname and their account number
						sender_lname = input("\n Please input sender surname: ")
						receiver_lname = input("\n Please input receiver surname: ")
						receiver_account_no = input("\n Please input receiver account number: ")
						self.transferMoney(sender_lname, receiver_lname, receiver_account_no, amount)
						break

			elif choice == 2: # customer account operations and profile settings
				while True: # loop doesn't end until the customer profile is found
					print('To go back input 999.')
					# searches for customer based on last name
					lname = input("\n Please input the customer's last name: ")
					if lname == '999': # to go back to the admin menu
						break
					# search for the customer and creates a customer object and opens the customer options menu
					msg, cust_obj = self.search_customers_by_name(lname=lname)
					print(msg)
					if cust_obj is not None: # if a customer is found then show them the customer options menu
						cust_obj.run_account_options(self.customer)

			elif choice == 3: # closing a user account
				if bool(admin_obj.has_full_admin_right()) is False: # checks if the user has full admin rights
					print('You do not have permissions to perform this action.')
				else:
					while True:
						lname = input("\n Please input the customer's last name: ")
						msg, cust_obj = self.search_customers_by_name(lname=lname)
						print(msg)
						if cust_obj is None: # if user not found then it takes them back the admin menu
							continue
						try: # attempts to remove the customer's row of information from the dataframe and updates the csv file
							self.customer.drop(self.customer[self.customer['lname'] == cust_obj.get_last_name()].index, inplace=True)
							self.customer.to_csv('customers.csv', index=False, sep=';')
						except KeyError as ke: # if incorrect dataframe structure
							print(f"Error updating customer data: {ke}")
						else:
							print(f'{cust_obj.get_first_name()} {cust_obj.get_last_name()} has been successfully'
								  f' removed from the system.')
							break

			elif choice == 4: # displays all customer details
				self.print_all_accounts_details()

			elif choice == 5:  # admin settings
				option = admin_obj.admin_settings()
				if option == 1: # change first name
					print(f'Current Name: {admin_obj.get_first_name()}, {admin_obj.get_last_name()}')
					while True:
						try: # catches any input that are numbers or special characters
							new_lname = input("\n Please input new Last Name: ")
							new_fname = input("\n Please input new First Name: ")
							if not new_lname.isalpha() or not new_lname.isalpha():
								raise ValueError("Input must contain letters only, no numbers or special characters.")
						except ValueError:
							print('Error. Please enter a valid name.')
							continue
						else: # changes the first and last names on the admin objects
							admin_obj.update_first_name(fname=new_fname,df=self.admin)
							admin_obj.update_last_name(lname=new_lname, df=self.admin)
							break

				elif option == 2: # change address
					while True:
						try: # makes sure that the address number is an integer
							hnumber = int(input("\nPlease enter the new address number: "))
						except ValueError:
							print('Error. Please enter a valid number.')
						else: # asks the user to input the rest of their address
							str_name = input("Please enter the new street name: ")
							city = input("Please enter the new city: ")
							post_code = input("Please enter the new postcode: ")

							address = f'{hnumber}, {str_name}, {city}, {post_code}'
							admin_obj.update_address(address, self.admin)
							break

				elif option == 3: # change username
					print(f'Current Username: {admin_obj.get_username()}')

					new_uname = input("\nPlease enter the new username: ")
					admin_obj.set_username(new_uname, self.admin)

				elif option == 4: # change password
					print(f'Current Password: {admin_obj.get_password()}')
					while True: # loop ends when new password is at least 4 characters long
						try:
							new_password = int(input("\nPlease enter the new password: "))
							if len(str(new_password)) < 4:
								print("Password must be at least 4 characters.")
								continue
						except ValueError:
							print('Error. Password must be a number.')
						else:
							admin_obj.update_password(new_password, self.admin)
							break
				elif option == 5: # show admin details
					admin_obj.show_details()

				elif option == 6: # to go back to admin menu
					continue
				else: # if the user inputs a number that isn't between 1 and 7
					print('Invalid option.')
					continue

			elif choice == 6: #managment report
				# The sum of all money the customers currently have in their accounts.
				total_money = self.customer['balance'].sum()
				# the sum of overdrafts taken by customers
				total_overdrafts = self.customer['overdraft_limit'].sum()
				# amount of customers in the system
				total_customers = self.customer.shape[0]

				# temporary column to hold the interest for each customer
				self.customer['interest'] = self.customer['balance'] * self.customer['interest_rate']
				# Calculate the total interest payable
				total_interest_payable = self.customer['interest'].sum()

				# Display the management report
				print("\n")
				print('Management Report')
				print(f'Total customers: {total_customers}')
				print(f'Total money: £{total_money}')
				print(f'Overdrafts: £{total_overdrafts}')
				print(f"Total Interest Payable: £{total_interest_payable}")

			elif choice == 7: # sign out
				loop = 0
				print("\n Exit account operations")
				self.run_main_options()
			else: # catches any input that isn't between 1 and 7
				print('Invalid option. Try again.')

	def print_all_accounts_details(self):
		"""Displays all the customer details in an ordered format"""
		for index, row in self.customer.iterrows():
			for col in self.customer.columns:
				print(f"{col}: {row[col]}")
			print()

try: # attempts to launch the banking app
	app = BankSystem()
	app.run_main_options()
except Exception as e: # generic exception handling
	print(f"An unexpected error occurred: {e}")

