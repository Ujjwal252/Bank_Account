# Bank Account Management & Transaction Analysis

> **Status: 🚧 In Progress — DataGrokr PLP Week 2 Mini-Project | Phase 2 Complete**

---

## Project Objective

This project will build a **Python-based Bank Account Management System** combined with a **pandas-powered Transaction Dataset Analysis** tool.

It demonstrates practical, real-world application of intermediate Python concepts taught in **DataGrokr Pre-Learning Program (PLP) Week 2**.

---

## DataGrokr PLP Week 2

This project is being developed as the **Week 2 mini-project** of the DataGrokr Pre-Learning Program.

It is built **phase by phase**, with each phase adding new features that correspond to the concepts covered in the weekly syllabus.

---

## Features

### Part A — OOP Bank Account System ✅ Implemented

- ✅ Account creation (account holder name, account number, initial balance)
- ✅ Deposit with validation
- ✅ Withdrawal with validation
- ✅ Balance management
- ✅ Transaction history tracking
- ✅ Exception handling (invalid amounts, insufficient balance)
- ✅ Unit tests (20 tests passing)

### Part B — Dataset Analysis 🔜 Planned

- 🔜 CSV transaction dataset (generated or imported)
- 🔜 Reading and exploring data with **pandas**
- 🔜 Filtering transactions by type, date, or amount
- 🔜 Aggregation using `groupby()`
- 🔜 Summary statistics (total deposits, total withdrawals, net balance)
- 🔜 Joining datasets using `merge()`
- 🔜 Numerical analysis using **NumPy**

### Python Concepts Demonstrated

> These concepts are applied where they naturally fit — not forced artificially.

- ✅ Object-Oriented Programming (Classes, `__init__`, class-level attributes)
- ✅ Modules and packages (`src/` as a package)
- ✅ Exception handling (`ValueError` with meaningful messages)
- ✅ Clean, readable code (PEP 8, docstrings, meaningful names)
- 🔜 Inheritance and Polymorphism (planned)
- 🔜 List comprehensions and dictionary comprehensions (planned)
- 🔜 `lambda`, `map()`, `filter()` (planned)
- 🔜 Decorators (planned)
- 🔜 Context managers (planned)

---

## Project Structure

```
Bank_Account/
│
├── README.md               ← This file
├── requirements.txt        ← Project dependencies
├── .gitignore              ← Files excluded from Git
├── run.py                  ← Entry point — run from project root
│
├── src/                    ← All Python source code
│   ├── __init__.py
│   │
│   ├── models/             ← OOP classes and data models
│   │   ├── __init__.py
│   │   └── bank_account.py ← ✅ BankAccount class (Phase 2)
│   │
│   ├── services/           ← Application/business logic (planned)
│   │   └── __init__.py
│   │
│   ├── analysis/           ← pandas/NumPy analysis (planned)
│   │   └── __init__.py
│   │
│   └── main.py             ← ✅ CLI demo (Phase 2)
│
├── data/                   ← CSV transaction datasets (planned)
│
└── tests/
    └── test_bank_account.py ← ✅ 20 unit tests (Phase 2)
```

### Folder Responsibilities

| Folder / File | Responsibility |
|---|---|
| `src/models/` | OOP class definitions (BankAccount, SavingsAccount, etc.) |
| `src/services/` | Business logic — deposit, withdrawal, validation rules |
| `src/analysis/` | pandas and NumPy-based transaction analysis |
| `data/` | CSV datasets for analysis |
| `tests/` | Unit tests for models and services |
| `src/main.py` | Entry point — orchestrates the application |

---

## Technologies

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core programming language |
| **pandas** | Data analysis and manipulation |
| **NumPy** | Numerical computations |
| **Git** | Version control |
| **GitHub** | Remote repository and collaboration |

---

## Setup Instructions

> These instructions will be updated as the project evolves.

```bash
# 1. Clone the repository
git clone <repo-url>
cd Bank_Account

# 2. Create and activate the virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# 3. Install dependencies (when requirements.txt is populated)
pip install -r requirements.txt
```

---

## Development Phases

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Project initialization & structure | ✅ Complete |
| Phase 2 | BankAccount OOP implementation | ✅ Complete |
| Phase 3 | pandas Transaction Analysis | 🔜 Planned |
| Phase 4 | Advanced features (decorators, context managers) | 🔜 Planned |
| Phase 5 | Testing & final cleanup | 🔜 Planned |

---

---

## Phase 2 — OOP Bank Account

### BankAccount Class (`src/models/bank_account.py`)

The `BankAccount` class is the core of Part A. Each instance represents one bank account.

#### Attributes

| Attribute | Type | Description |
|---|---|---|
| `account_holder` | `str` | Name of the account owner |
| `account_number` | `str` | Auto-generated unique ID (e.g. `ACC1001`) |
| `balance` | `float` | Current account balance |
| `_transactions` | `list` | Private list of all successful transactions |

#### How Account Numbers are Generated

A **class-level counter** `_account_counter` starts at `1000`. Each time a new `BankAccount` is created, the counter increments and the account number is formatted as `f"ACC{counter}"`. This ensures every account in a program session gets a distinct number without needing a database.

#### Methods

| Method | Description |
|---|---|
| `__init__(account_holder, initial_balance=0.0)` | Creates a new account, validates initial balance |
| `deposit(amount)` | Adds funds, validates amount > 0, records transaction |
| `withdraw(amount)` | Removes funds, validates amount > 0 and ≤ balance |
| `get_balance()` | Returns current balance (does not print) |
| `get_transaction_history()` | Returns a **copy** of the transaction list |
| `display_account()` | Prints account holder, number, and balance |

#### Transaction History

Every successful operation (initial deposit, deposit, withdrawal) is recorded as a dictionary:

```python
{"type": "deposit", "amount": 2000.0, "balance": 7000.0}
```

`get_transaction_history()` returns a **copy** of the internal list, so callers cannot accidentally modify the real history.

#### Exception Handling

All validation uses `ValueError` with clear messages:

| Situation | Exception |
|---|---|
| Negative initial balance | `ValueError("Initial balance cannot be negative.")` |
| Deposit ≤ 0 | `ValueError("Deposit amount must be greater than zero.")` |
| Withdrawal ≤ 0 | `ValueError("Withdrawal amount must be greater than zero.")` |
| Withdrawal > balance | `ValueError("Insufficient balance.")` |

### Tests (`tests/test_bank_account.py`)

20 unit tests across 4 test classes using Python's built-in `unittest` framework:

- `TestBankAccountCreation` — account creation and account number uniqueness
- `TestDeposit` — valid deposits, invalid amounts, balance unchanged on error
- `TestWithdraw` — valid withdrawals, invalid amounts, insufficient balance
- `TestTransactionHistory` — history growth, copy isolation

**All 20 tests pass.**

### Running the Project

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run the demo
python run.py

# Run the tests
python -m unittest tests/test_bank_account.py -v
```

---

*DataGrokr Pre-Learning Program — Week 2 Mini-Project*
