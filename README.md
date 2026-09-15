# Bank Account Management & Transaction Analysis

## Project Overview

This project is a Python-based **Bank Account Management System** integrated with a **pandas-powered Transaction Dataset Analysis** suite. It was developed to systematically implement and demonstrate the syllabus topics outlined in the **DataGrokr Pre-Learning Program **.

## Objective

To build an object-oriented, clean-coded banking simulation (Part A) paired with a functional data analysis pipeline (Part B) that satisfies all DataGrokr Week 2 requirements. The focus is on clean architecture, isolated exception design, and strict test-driven integrity.

## Features

- **OOP Core:** Bank account creation, constraints, deposits, and validated withdrawals.
- **Inheritance & Polymorphism:** Specialized account models (e.g., `SavingsAccount`) with strict minimum balance requirements overlapping standard validation.
- **Advanced Python Subsystems:** Custom logging via decorators (`@log_transaction`), flat-file IO managed securely through context managers (`TransactionLogger`), and functional paradigms (`lambda`, `map`, `filter`, comprehensions) used natively on dataset dictionaries.
- **pandas/NumPy Analysis:** Data extraction using `pd.read_csv`, dimensional aggregation via `groupby`, statistical volume tracking in `NumPy`, and ledger merging.
- **Persistence:** Interactive customer records and timestamped transactions are stored in `data/master_customer_report.csv` and restored when the application starts.
- **Account operations:** Existing customers can be selected by customer ID or account number for deposits, withdrawals, balance checks, history, and account views.
- **Money safety:** Balances use `Decimal`, reject non-finite values, and enforce age, ID, opening-balance, and savings minimum-balance rules.
- **Safe storage:** Master CSV updates use atomic replacement, and successful operations are appended to the runtime transaction log.
- **Live analytics:** The CLI reports customer count, transaction count, deposits, withdrawals, net movement, and combined balance from current customer records.
- **Resiliency:** Granular exception handling (never swallowing exceptions arbitrarily) backed by the project test suite via Python `unittest`.

---

## Concepts Demonstrated


## 📚 Python Concepts Covered

| Concept | Implementation |
|---|---|
| **Comprehensions** | List and dictionary comprehensions |
| **Lambda** | Inline functions for filtering and formatting |
| **map()** | Applies functions to transaction records |
| **filter()** | Filters records based on conditions |
| **OOP** | `BankAccount` class, attributes, and methods |
| **Inheritance** | `SavingsAccount` extends `BankAccount` |
| **Polymorphism** | Overridden `withdraw()` method |
| **Decorators** | `@log_transaction` for transaction logging |
| **Context Managers** | `TransactionLogger` for safe file handling |
| **pandas** | CSV loading, filtering, `groupby()`, `merge()` |
| **NumPy** | Transaction statistics and calculations |
| **Modules & Packages** | Structured Python project organization |
| **Virtual Environment** | Isolated project environment using `venv` |
| **Exception Handling** | Validation and file-related errors |
| **Clean Code** | Modular, readable, and maintainable structure |

## Project Structure

```
Bank_Account/
├── .gitignore              ← Excludes runtime logs and venv
├── README.md               ← Documentation
├── requirements.txt        ← Locked 3rd party modules (pandas, numpy)
├── run.py                  ← Root Execution Script
├── src/                    ← Application Packages
│   ├── main.py             ← CLI application interface
│   ├── analysis/           
│   │   ├── __init__.py
│   │   └── transaction_analysis.py 
│   ├── models/             
│   │   ├── __init__.py
│   │   └── bank_account.py 
│   └── services/           
│       ├── __init__.py
│       ├── decorators.py   
│       └── transaction_logger.py 
├── data/
│   ├── accounts.csv        ← Analytics fixture: account-level records
│   ├── transactions.csv    ← Analytics fixture: ledger entries (25 rows)
│   └── master_customer_report.csv ← Runtime customer and transaction records
└── tests/
    ├── test_bank_account.py
    ├── test_decorators.py
    ├── test_transaction_analysis.py
    └── test_transaction_logger.py
```

---

## Installation

1. **Clone the generic repository**:
   ```powershell
   git clone <repo-url>
   cd Bank_Account
   ```
2. **Setup virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Requirements**:
   ```powershell
   python -m pip install -r requirements.txt
   ```

---

## Running the Application

Execute the application orchestration from the project root simply:
```powershell
python run.py
```

The application menu accepts either numbered options or operation names. Existing accounts can be opened from `view customers`, and the `analytics` option summarizes live customer data.

## Running Tests

Verify the underlying systems using the built-in isolated unittests.
```powershell
python -m unittest discover -s tests -v
```

---

## Dataset Description

The `data/` folder contains two separate kinds of data:
- **Analytics fixtures:** `transactions.csv` and `accounts.csv` are the sample datasets used by the pandas/NumPy analysis module and its tests. Keep both files unless the analytics feature and its tests are removed as well.
- **Runtime data:** `master_customer_report.csv` is the live customer database written by the interactive application. It is loaded on startup and should be backed up before deletion.
- **Runtime log:** `app_transaction_log.txt` records successful deposits and withdrawals. It is regenerated automatically when the first operation is completed.

## Exception Handling

All structural mutations (depositing negative volumes, breaching minimum balances in SavingsAccounts, file absences in CSV loads) instantly raise explicit typed exceptions.

We do NOT use custom exceptions arbitrarily because Python's built-in `ValueError` and `FileNotFoundError` semantically resolve these boundaries securely. The program deliberately propagates exceptions upwards (decorators don't swallow exceptions and context managers natively return `False` on escape sequences) making the software predictable.

---

## Development Phases

This project was developed incrementally spanning:
- **Phase 1:** Bootstrapping project architecture & Git rules.
- **Phase 2:** OOP foundation (`BankAccount`) and exception design.
- **Phase 3:** Transaction Analytics mapping Pandas and NumPy functionality to a generic UI schema.
- **Phase 4:** Incorporating intercept hooks natively across context managers and dynamic decorators seamlessly handling IO bindings.
- **Phase 5:** Formal integration audit satisfying Week 2 PLP prerequisites (Comprehensions, Lambda, Map, Filter, Polymorphism).

---
*Created for DataGrokr Pre-Learning Program — Week 2*
