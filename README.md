# 🏦 Banking Management System

A command-line banking application built with **Python**. It supports customer accounts, secure PIN login, deposits, withdrawals, money transfers, and an admin panel, with all data stored in a local JSON file.

---

## ✨ Features

### Customer
- **Create account**: auto-generated account number, initial deposit, and a 4-digit PIN
- **Secure login**: PINs are hashed with **bcrypt** (never stored in plain text)
- **Account lock**: the account is locked after 3 wrong PIN attempts
- **Account details** and **balance enquiry**
- **Deposit** and **withdraw** money with validation
- **Transfer money** to another account (shows receiver name before confirming, blocks transfers to locked or own accounts)
- **Change PIN** (requires the current PIN)
- **Transaction history** with type, amount, date/time, and sender/receiver details

### Admin
- **View all accounts** with balance and status (Active / Locked)
- **Unlock accounts** that were locked after failed login attempts

---

## 🛠️ Tech Stack

| Component | Used for |
|-----------|----------|
| Python 3.8+ | Core language |
| `bcrypt` | PIN hashing and verification |
| `json` | Persistent data storage |
| `os` | Checking whether the data file exists |
| `datetime` | Transaction timestamps |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install the dependency
```bash
pip install bcrypt
```

### 3. Run the application
```bash
python main.py
```
> Replace `main.py` with your actual file name.

The data file `bank_data.json` is created automatically when the first account is made.

---

## 📖 Usage

### Main menu
```
========== BANKING MANAGEMENT SYSTEM ==========
1. Create Account
2. Customer Login
3. Admin Login
4. Exit
```

### Customer dashboard
```
===== CUSTOMER DASHBOARD =====
1. Account Details
2. Check Balance
3. Deposit Money
4. Withdraw Money
5. Transaction History
6. Change PIN
7. Transfer Money
8. Logout
```

### Admin dashboard
```
===== ADMIN DASHBOARD =====
1. View All Accounts
2. Unlock Account
3. Logout
```

**Default admin credentials (for demo only):** `admin` / `admin123`

---

## 🗂️ Data Structure

Accounts are stored in `bank_data.json`, keyed by account number:

```json
{
    "100001": {
        "name": "Manikanta",
        "age": 21,
        "balance": 5000.0,
        "pin_hash": "$2b$12$...",
        "failed_attempts": 0,
        "locked": false,
        "transactions": [
            {
                "type": "Initial Deposit",
                "amount": 5000.0,
                "date": "2026-11-13 10:30:00"
            }
        ]
    }
}
```

Transfer records additionally store `to_account` / `to_name` (sender side) or `from_account` / `from_name` (receiver side).

---

## 🧠 How It Works

1. **Load and save**: every operation loads the JSON file, modifies the data in memory, and saves it back.
2. **Account numbers**: start at `100001` and increment from the highest existing number.
3. **PIN security**: `bcrypt.hashpw()` hashes the PIN with a random salt, and `bcrypt.checkpw()` verifies it at login.
4. **Lockout logic**: failed attempts are saved to the file, so closing and reopening the program does not reset them.
5. **Transfers**: both balances and both transaction histories are updated before a single save.

---

## 📁 Project Structure

```
.
├── main.py           # Application source code
├── bank_data.json    # Auto-generated data file
└── README.md
```

---

## ⚠️ Known Limitations

- Admin credentials are hardcoded (fine for a demo, not for production).
- Non-numeric input for age or amounts can crash the program, since there is no `try/except` around `int()` / `float()`.
- JSON file storage is not safe for multiple users writing at the same time.
- Money is stored as `float`, which can cause rounding issues in real-world banking.

## 🔮 Future Improvements

- Move to a database such as SQLite or PostgreSQL
- Store admin credentials as a hashed value in a config or environment file
- Add input validation with `try/except`
- Use `Decimal` for currency handling
- Add a GUI or web interface (Flask / FastAPI)
- Add unit tests

---

## 👤 Author

**Manikanta Avula**

---

## 📄 License

This project is for educational purposes. Add a license of your choice (e.g., MIT) if you plan to share it publicly.
