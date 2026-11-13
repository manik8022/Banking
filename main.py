
import json
import os
import bcrypt
from datetime import datetime

DATA_FILE = "bank_data.json"


# 1. Load account data
def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, OSError):
        return {}


# 2. Save account data
def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


# 3. Hash PIN using bcrypt
def hash_pin(pin):
    hashed_pin = bcrypt.hashpw(
        pin.encode("utf-8"),
        bcrypt.gensalt()
    )
    return hashed_pin.decode("utf-8")


# 4. Verify PIN
def verify_pin(pin, customer):
    stored_hash = customer["pin_hash"].encode("utf-8")
    return bcrypt.checkpw(pin.encode("utf-8"), stored_hash)


# 5. Generate account number
def generate_account_number(accounts):
    if not accounts:
        return "100001"

    numbers = [int(number) for number in accounts.keys()]
    return str(max(numbers) + 1)


# 6. Create account
def create_account():
    accounts = load_accounts()

    print("\n--- CREATE BANK ACCOUNT ---")

    name = input("Enter customer name: ")
    age = int(input("Enter customer age: "))
    initial_deposit = float(input("Enter initial deposit: "))

    if age <= 0 or initial_deposit < 0:
        print("Invalid age or deposit amount!")
        return

    pin = input("Create 4-digit PIN: ")

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must contain exactly 4 digits!")
        return

    account_number = generate_account_number(accounts)

    accounts[account_number] = {
        "name": name,
        "age": age,
        "balance": initial_deposit,
        "pin_hash": hash_pin(pin),
        "failed_attempts": 0,
        "locked": False,
        "transactions": [
            {
                "type": "Initial Deposit",
                "amount": initial_deposit,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    }

    save_accounts(accounts)

    print("\nAccount created successfully!")
    print("Your Account Number:", account_number)


# 7. Customer login
def customer_login():
    accounts = load_accounts()

    print("\n--- CUSTOMER LOGIN ---")

    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    customer = accounts[account_number]

    if customer["locked"]:
        print("Your account is locked. Contact admin.")
        return

    for attempt in range(3):
        pin = input("Enter your 4-digit PIN: ")

        if verify_pin(pin, customer):
            customer["failed_attempts"] = 0
            save_accounts(accounts)

            print("\nLogin successful!")
            customer_dashboard(account_number)
            return

        customer["failed_attempts"] += 1
        remaining = 3 - customer["failed_attempts"]

        print("Incorrect PIN!")

        if remaining > 0:
            print("Attempts remaining:", remaining)

        if customer["failed_attempts"] >= 3:
            customer["locked"] = True
            save_accounts(accounts)
            print("Account locked after 3 incorrect attempts!")
            return

        save_accounts(accounts)


# 8. Account details
def account_details(account_number):
    accounts = load_accounts()
    customer = accounts[account_number]

    print("\n--- ACCOUNT DETAILS ---")
    print("Account Number:", account_number)
    print("Customer Name:", customer["name"])
    print("Age:", customer["age"])
    print("Balance: Rs.", customer["balance"])


# 9. Balance enquiry
def check_balance(account_number):
    accounts = load_accounts()
    customer = accounts[account_number]

    print("\nAvailable Balance: Rs.", customer["balance"])


# 10. Deposit money
def deposit_money(account_number):
    accounts = load_accounts()
    customer = accounts[account_number]

    amount = float(input("Enter deposit amount: "))

    if amount <= 0:
        print("Enter a valid amount!")
        return

    customer["balance"] += amount

    customer["transactions"].append({
        "type": "Deposit",
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_accounts(accounts)

    print("Deposit successful!")
    print("Updated Balance: Rs.", customer["balance"])


# 11. Withdraw money
def withdraw_money(account_number):
    accounts = load_accounts()
    customer = accounts[account_number]

    amount = float(input("Enter withdrawal amount: "))

    if amount <= 0:
        print("Enter a valid amount!")
        return

    if amount > customer["balance"]:
        print("Insufficient balance!")
        return

    customer["balance"] -= amount

    customer["transactions"].append({
        "type": "Withdrawal",
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_accounts(accounts)

    print("Withdrawal successful!")
    print("Remaining Balance: Rs.", customer["balance"])


# 12. Money transfer
def transfer_money(account_number):
    accounts = load_accounts()

    sender = accounts[account_number]

    print("\n--- MONEY TRANSFER ---")

    receiver_account = input("Enter receiver account number: ")

    if receiver_account not in accounts:
        print("Receiver account not found!")
        return

    if receiver_account == account_number:
        print("You cannot transfer money to your own account!")
        return

    receiver = accounts[receiver_account]

    if receiver["locked"]:
        print("Receiver account is locked. Transfer cannot be completed!")
        return

    print("Receiver Name:", receiver["name"])

    amount = float(input("Enter transfer amount: "))

    if amount <= 0:
        print("Enter a valid transfer amount!")
        return

    if amount > sender["balance"]:
        print("Insufficient balance!")
        return

    # Update both account balances
    sender["balance"] -= amount
    receiver["balance"] += amount

    transfer_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sender transaction history
    sender["transactions"].append({
        "type": "Transfer Sent",
        "amount": amount,
        "to_account": receiver_account,
        "to_name": receiver["name"],
        "date": transfer_date
    })

    # Receiver transaction history
    receiver["transactions"].append({
        "type": "Transfer Received",
        "amount": amount,
        "from_account": account_number,
        "from_name": sender["name"],
        "date": transfer_date
    })

    save_accounts(accounts)

    print("\nMoney transferred successfully!")
    print("Transferred Amount: Rs.", amount)
    print("Receiver Name:", receiver["name"])
    print("Receiver Account:", receiver_account)
    print("Remaining Balance: Rs.", sender["balance"])


# 13. Change PIN
def change_pin(account_number):
    accounts = load_accounts()
    customer = accounts[account_number]

    old_pin = input("Enter current PIN: ")

    if not verify_pin(old_pin, customer):
        print("Incorrect current PIN!")
        return

    new_pin = input("Enter new 4-digit PIN: ")

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must contain exactly 4 digits!")
        return

    customer["pin_hash"] = hash_pin(new_pin)
    save_accounts(accounts)

    print("PIN changed successfully!")


# 14. Transaction history
def transaction_history(account_number):
    accounts = load_accounts()
    customer = accounts[account_number]

    print("\n--- TRANSACTION HISTORY ---")

    if not customer["transactions"]:
        print("No transactions found.")
        return

    for transaction in customer["transactions"]:
        print("\n---------------------------")
        print("Transaction Type:", transaction["type"])

        if transaction["type"] == "Transfer Sent":
            receiver_account = transaction.get("to_account", "")
            receiver_name = transaction.get("to_name")

            # Find name for older transfer records
            if not receiver_name and receiver_account in accounts:
                receiver_name = accounts[receiver_account]["name"]

            print("Sent To:", receiver_name or "Name not available")
            print("Receiver Account:", receiver_account)

        elif transaction["type"] == "Transfer Received":
            sender_account = transaction.get("from_account", "")
            sender_name = transaction.get("from_name")

            # Find name for older transfer records
            if not sender_name and sender_account in accounts:
                sender_name = accounts[sender_account]["name"]

            print("Received From:", sender_name or "Name not available")
            print("Sender Account:", sender_account)

        print("Amount: Rs.", transaction["amount"])
        print("Date & Time:", transaction["date"])

    print("\n---------------------------")


# 15. Customer dashboard
def customer_dashboard(account_number):
    while True:
        print("\n===== CUSTOMER DASHBOARD =====")
        print("1. Account Details")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Transfer Money")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            account_details(account_number)

        elif choice == "2":
            check_balance(account_number)

        elif choice == "3":
            deposit_money(account_number)

        elif choice == "4":
            withdraw_money(account_number)

        elif choice == "5":
            transaction_history(account_number)

        elif choice == "6":
            change_pin(account_number)

        elif choice == "7":
            transfer_money(account_number)

        elif choice == "8":
            print("Logged out successfully!")
            break

        else:
            print("Invalid choice!")


# 16. Admin login
def admin_login():
    print("\n--- ADMIN LOGIN ---")

    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        print("\nAdmin login successful!")
        admin_dashboard()
    else:
        print("Invalid admin credentials!")


# 17. View all customer accounts
def view_all_accounts():
    accounts = load_accounts()

    print("\n========== ALL CUSTOMER ACCOUNTS ==========")

    if not accounts:
        print("No accounts available.")
        return

    for account_number, customer in accounts.items():
        status = "Locked" if customer["locked"] else "Active"

        print("-------------------------------------------")
        print("Account Number:", account_number)
        print("Customer Name:", customer["name"])
        print("Customer Age:", customer.get("age", "Not available"))
        print("Balance: Rs.", customer["balance"])
        print("Account Status:", status)

    print("-------------------------------------------")


# 18. Unlock account
def unlock_account():
    accounts = load_accounts()

    account_number = input("Enter account number to unlock: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    accounts[account_number]["locked"] = False
    accounts[account_number]["failed_attempts"] = 0

    save_accounts(accounts)

    print("Account unlocked successfully!")


# 19. Admin dashboard
def admin_dashboard():
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. View All Accounts")
        print("2. Unlock Account")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_accounts()

        elif choice == "2":
            unlock_account()

        elif choice == "3":
            print("Admin logged out successfully!")
            break

        else:
            print("Invalid choice!")


# 20. Main menu
def main():
    while True:
        print("\n========== BANKING MANAGEMENT SYSTEM ==========")
        print("1. Create Account")
        print("2. Customer Login")
        print("3. Admin Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            customer_login()

        elif choice == "3":
            admin_login()

        elif choice == "4":
            print("Thank you for using our Banking System!")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
