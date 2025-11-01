A secure and modular command-line banking application built with Python. This project simulates core banking operations, demonstrating principles of object-oriented programming, data persistence, and transaction management in a console-based interface.

Features
User Authentication: Secure login system for customers.

Account Management: View account details and check balances.

Financial Transactions:

Deposit funds into your account.

Withdraw funds with balance validation.

Transfer money to other registered customers.

Transaction History: View a detailed log of all past transactions.

Data Persistence: Customer and transaction data is saved to and loaded from JSON files for persistence between sessions.

Clean CLI Interface: A user-friendly menu-driven console interface.

Technology Stack
Language: Python

Data Storage: JSON files (customers.json, transactions.json)

Key Concepts: Object-Oriented Programming (OOP), File I/O, Data Serialization

bankapp/
├── src/
│   ├── __init__.py
│   ├── bank.py           # Main application logic and menu flow
│   ├── customer.py       # Customer class definition
│   └── transaction.py    # Transaction class definition
├── data/
│   ├── customers.json      # Stores customer account data
│   └── transactions.json   # Stores all transaction records
├── main.py               # Application entry point
└── README.md

How It Works
The application is built around two main classes:

Customer: Manages customer attributes like name, customer ID, PIN, and account balance.

Transaction: Creates records for every financial action, storing details like type, amount, timestamp, and involved parties.

All data is serialized to JSON files, ensuring that customer information and transaction history are preserved after the program exits.
