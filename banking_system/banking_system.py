import os
import datetime

data_directory = "bank_data"

# Create directory if it does not exist
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# File paths
users_file = os.path.join(data_directory, "users.txt")
transactions_file = os.path.join(data_directory, "transactions.txt")

# Constants
SAVINGS_MIN_BALANCE = 100
CURRENT_MIN_BALANCE = 500

def user_login():
    print("\n-----Banking System-----")
    print("1. Admin Login")
    print("2. Customer Login")
    print("3. Exit")
    option = int(input("Enter your option:\t"))
    if option == 1:
        username = input("Enter your user id:\t")
        password = input("Enter your password:\t")
        return username, password, "admin"
    elif option == 2:
        customer_id = input("Enter your account number:\t")
        password = input("Enter your password:\t")
        return customer_id, password, "customer"
    elif option == 3:
        print("Exiting...")
        return None, None, None
    else:
        print("Invalid Option! Please try again.")
        return user_login()


def admin_menu(username, password):
    if username == "admin" and password == "admin123":
        while True:
            print("\n-----Bank Admin Menu-----")
            print("1. Create a Staff Account")
            print("2. Create a Customer Account")
            print("3. View All Accounts")
            print("4. Update An Account")
            print("5. Generate Customer Statement")
            print("6. Exit")
            option = int(input("Enter an Option:\t"))

            if option == 1:
                create_staff_account()
            elif option == 2:
                create_customer_account()
            elif option == 3:
                view_all_accounts()
            elif option == 4:
                account_number = input("Enter account number:\t")
                update_account(account_number)
            elif option == 5:
                account_number = input("Enter account number:\t")
                start_date = input("Enter start date (YYYY-MM-DD):\t")
                end_date = input("Enter end date (YYYY-MM-DD):\t")
                generate_statement(account_number, start_date, end_date)
            elif option == 6:
                print("Exiting Bank Admin Menu...")
                break
            else:
                print("Invalid Option! Please try again.")
    else:
        print("Invalid admin credentials!")

def customer_menu(account_number, password):
    users = load_users()
    if account_number in users and users[account_number]['password'] == password:
        while True:
            print(f"\n-----Bank User Menu (Welcome, {users[account_number]['name']})-----")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Statements")
            print("5. Change Password")
            print("6. Exit")
            choice = int(input("Enter your choice:\t"))

            if choice == 1:
                checking_balance(account_number)
            elif choice == 2:
                amount = float(input("Enter amount to deposit:\t"))
                deposit_money(account_number, amount)
            elif choice == 3:
                amount = float(input("Enter amount to withdraw:\t"))
                withdraw_money(account_number, amount)
            elif choice == 4:
                start_date = input("Enter start date (YYYY-MM-DD):\t")
                end_date = input("Enter end date (YYYY-MM-DD):\t")
                generate_statement(account_number, start_date, end_date)
            elif choice == 5:
                change_password(account_number)
            elif choice == 6:
                print("Exiting Bank User Menu...")
                break
            else:
                print("Invalid Choice! Please try again.")
    else:
        print("Invalid account number or password! Please try again.")

def create_staff_account():
    username = input("Enter staff username: ")
    password = input("Enter staff password: ")
    staff_details = f"{username}, {password}, staff\n"
    with open(users_file, "a") as file:
        file.write(staff_details)
    print(f"Staff account created successfully for {username}.")

def create_customer_account():
    name = input("Enter customer name: ")
    address = input("Enter customer address: ")
    contact_number = input("Enter contact number: ")
    citizenship = input("Enter citizenship number: ")
    father_name = input("Enter father's name: ")
    grandfather_name = input("Enter grandfather's name: ")
    mother_name = input("Enter mother's name: ")
    
    account_type = input("Enter account type (Savings/Current): ").lower()
    while account_type not in ['savings', 'current']:
        print("Invalid account type. Please enter 'Savings' or 'Current'.")
        account_type = input("Enter account type (Savings/Current): ").lower()
    
    initial_balance = float(input("Enter initial balance: "))
    min_balance = SAVINGS_MIN_BALANCE if account_type == 'savings' else CURRENT_MIN_BALANCE
    if initial_balance < min_balance:
        print(f"Initial balance must be at least RS {min_balance} for {account_type.capitalize()} account.")
        return

    account_number = get_new_account_number()
    password = "customer123"  # Default password
    account_details = f"{account_number},{name},{password},customer, {account_type}, {initial_balance}, {address}, {contact_number}, {citizenship}, {father_name}, {grandfather_name}, {mother_name}\n"
    with open(users_file, "a") as file:
        file.write(account_details)
    print(f"Account created successfully! Account number is {account_number}.")
    print(f"Default password is: {password}")

def deposit_money(account_number, amount):
    users = load_users()
    if account_number in users:
        users[account_number]['balance'] += amount
        save_users(users)
        save_transaction(account_number, 'deposit', amount)
        print(f"Deposited Rs{amount:.2f}. New balance is Rs{users[account_number]['balance']:.2f}.")
    else:
        print("Account not found!")

def withdraw_money(account_number, amount):
    users = load_users()
    if account_number in users:
        current_balance = users[account_number]['balance']
        account_type = users[account_number]['account_type']
        min_balance = SAVINGS_MIN_BALANCE if account_type == 'savings' else CURRENT_MIN_BALANCE
        if current_balance - amount >= min_balance:
            users[account_number]['balance'] -= amount
            save_users(users)
            save_transaction(account_number, 'withdrawal', amount)
            print(f"Withdrew Rs{amount:.2f}. New balance is Rs{users[account_number]['balance']:.2f}.")
        else:
            print(f"Insufficient Balance! Minimum balance of Rs{min_balance} must be maintained.")
    else:
        print("Account not found!")

def checking_balance(account_number):
    users = load_users()
    if account_number in users:
        print(f"Your balance is Rs{users[account_number]['balance']:.2f}.")
    else:
        print("Account not found!")

def generate_statement(account_number, start_date, end_date):
    users = load_users()
    if account_number not in users:
        print("Account not found!")
        return

    try:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date foRsat. Please use YYYY-MM-DD.")
        return

    transactions = load_transactions()
    print(f"\nStatement for Account {account_number} ({start_date} to {end_date}):")
    print("Date        | Transaction Type | Amount")
    print("-----------------------------------------")
    total_deposits = 0
    total_withdrawals = 0
    for transaction in transactions:
        if transaction[0] == account_number:
            trans_date = datetime.datetime.strptime(transaction[1], "%Y-%m-%d").date()
            if start <= trans_date <= end:
                print(f"{transaction[1]} | {transaction[2]:16} | Rs{float(transaction[3]):.2f}")
                if transaction[2] == 'deposit':
                    total_deposits += float(transaction[3])
                elif transaction[2] == 'withdrawal':
                    total_withdrawals += float(transaction[3])
    print("-----------------------------------------")
    print(f"Total Deposits:    Rs{total_deposits:.2f}")
    print(f"Total Withdrawals: Rs{total_withdrawals:.2f}")

def load_users():
    users = {}
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    account_number, name, password, account_class, account_type, *rest = parts
                    balance = float(rest[0]) if len(rest) > 1 else 0.0
                    address = rest[1] if len(rest) > 2 else ""
                    contact_number = rest[2] if len(rest) > 3 else ""
                    citizenship = rest[3] if len(rest)> 4 else ""
                    father_name= rest[4] if len(rest)> 5 else ""
                    grandfather_name = rest[5] if len(rest)> 6 else ""
                    mother_name = rest[6] if len(rest)> 7 else ""
                     
                    users[account_number] = {
                        'name': name, 
                        'password': password, 
                        'account_class': account_class,
                        'account_type': account_type, 
                        'balance': balance,
                        'address': address,
                        'contact_number': contact_number,
                        'citizenship': citizenship,
                        'father_name': father_name,
                        'grandfather_name': grandfather_name,
                        'mother_name': mother_name 
                    }
    return users

def save_users(users):
    with open(users_file, 'w') as file:
        for account_number, details in users.items():
            file.write(f"{account_number},{details['name']},{details['password']},{details['account_type']},{details['balance']},{details['address']}\n")

def load_transactions():
    transactions = []
    if os.path.exists(transactions_file):
        with open(transactions_file, 'r') as file:
            for line in file:
                transactions.append(line.strip().split(','))
    return transactions

def save_transaction(account_number, transaction_type, amount):
    with open(transactions_file, 'a') as file:
        file.write(f"{account_number},{datetime.date.today()},{transaction_type},{amount}\n")

def get_new_account_number():
    users = load_users()
    return str(1000 + len(users) + 1)

def update_account(account_number):
    users = load_users()
    if account_number in users:
        print("1. Edit address")
        print("2. Edit password")
        print("3. Edit Contact Number")
        choice = int(input("Enter your choice:\t"))
        if choice == 1:
            new_address = input("Enter new address:\t")
            users[account_number]['address'] = new_address
            save_users(users)
            print("Address updated successfully!")
        elif choice == 2:
            new_password = input("Enter new password:\t")
            users[account_number]['password'] = new_password
            save_users(users)
            print("Password updated successfully!")
        elif choice == 3:
            new_contact_number = input("Enter new contact number:\t")
            users[account_number]['contact_number'] = new_contact_number
            save_users(users)
            print("Contact number updated successfully!")
        else:
            print("Invalid choice!")
    else:
        print("Account not found!")

def change_password(account_number):
    users = load_users()
    if account_number in users:
        old_password = input("Enter your current password: ")
        if old_password == users[account_number]['password']:
            new_password = input("Enter new password: ")
            configure_password = input("Configure new password: ")
            if new_password == configure_password:
                users[account_number]['password'] = new_password
                save_users(users)
                print("Password changed successfully!")
            else:
                print("Passwords do not match. Password change failed.")
        else:
            print("Incorrect current password. Password change failed.")
    else:
        print("Account not found!")

def view_all_accounts():
    users = load_users()
    if users:
        print("Account Number | Name | Account Type | Balance | Address | Contact Number | Citizenship | Father's Name | Grandfather's Name | Mother's Name")
        print("---------------------------------------------------------------------------------------------------------------------------------------------")
        for account_number, details in users.items():
                print(f"{account_number} | {details['name']} | {details['account_type']} | Rs{details['balance']:.2f} | {details['address']} | {details['contact_number']} | {details['citizenship']} | {details['father_name']} | {details['grandfather_name']} | {details['mother_name']}")
    else:
        print("No accounts found.")

# Main loop
while True:
    username, password, role = user_login()
    if role == "admin":
        admin_menu(username, password)
    elif role == "customer":
        customer_menu(username, password)
    elif username is None and password is None and role is None:
        break