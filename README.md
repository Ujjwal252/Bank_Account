# Bank Account Management & Transaction Analysis

## Project Overview

This project is a Python-based **Bank Account Management System** integrated with a **pandas-powered Transaction Dataset Analysis** suite. It was developed to systematically implement and demonstrate the syllabus topics outlined in the **DataGrokr Pre-Learning Program (PLP) Week 2**.

## Objective

To build an object-oriented, clean-coded banking simulation (Part A) paired with a functional data analysis pipeline (Part B) that satisfies all DataGrokr Week 2 requirements. The focus is on clean architecture, isolated exception design, and strict test-driven integrity.

## Features

- **OOP Core:** Bank account creation, constraints, deposits, and validated withdrawals.
- **Inheritance & Polymorphism:** Specialized account models (e.g., `SavingsAccount`) with strict minimum balance requirements overlapping standard validation.
- **Advanced Python Subsystems:** Custom logging via decorators (`@log_transaction`), flat-file IO managed securely through context managers (`TransactionLogger`), and functional paradigms (`lambda`, `map`, `filter`, comprehensions) used natively on dataset dictionaries.
- **pandas/NumPy Analysis:** Data extraction using `pd.read_csv`, dimensional aggregation via `groupby`, statistical volume tracking in `NumPy`, and ledger merging.
- **Resiliency:** Granular exception handling (never swallowing exceptions arbitrarily) backed by 39 robust unit tests via Python `unittest`.

---

## Week 2 Concepts Demonstrated

| Week 2 Concept | Where Demonstrated |
| :--- | :--- |
| **Comprehensions** | `transaction_analysis.py`: Extracts specific deposit lists (List); Maps grouped accounts to Series dicts (Dict). |
| **lambda** | `transaction_analysis.py`: Inline predicates checking transaction keys (`x["TransactionType"] == ...`) and mapping formatter strings. |
| **map** | `transaction_analysis.py`: Applies string interpolation across a filtered list of large accounts. |
| **filter** | `transaction_analysis.py`: Sifts `dict` records extracting only "Withdrawal"s or values > 5000 natively. |
| **OOP** | `bank_account.py`: Classes, attributes, and methods in `BankAccount`. Defines `__init__`, encapsulate state (`_transactions`). |
| **Inheritance** | `bank_account.py`: `SavingsAccount(BankAccount)` inherits standard logic but introduces a `minimum_balance`. |
| **Polymorphism** | `bank_account.py`: `SavingsAccount.withdraw()` overwrites parent generic logic enforcing distinct minimum balance rules. |
| **Decorators** | `decorators.py`: `@log_transaction` adorns class operations tracing function start, argument extraction `*args, **kwargs`, and re-raising of errors securely. Uses `functools.wraps`. |
| **Context Managers** | `transaction_logger.py`: `TransactionLogger` natively secures append bindings to `.txt` files in `__enter__` and strictly closes streams regardless of exceptions in `__exit__`. |
| **pandas** | `transaction_analysis.py`: Uses `pd.read_csv` (loads assets), `df.groupby(...).agg(...)` (calculates user dimensions), and `pd.merge` (joins ledger types). |
| **NumPy** | `transaction_analysis.py`: Harnesses `np.sum()`, `np.mean()`, `np.max()`, and `np.min()` operating strictly over localized `amount` arrays. |
| **Modules** | General: Imports separated intelligently. Features abstracted loosely (e.g. `main.py` explicitly loads exactly what it orchestrates). |
| **Packages** | `src/`: Organizes hierarchical folders containing `__init__.py` making imports clean (`src.models.bank_account`, `src.analysis.transaction_analysis`). |
| **Virtual Environment** | Environmentally walled project. See Installation. Excluded entirely from `git` via `.gitignore`. |
| **Clean Code** | PEP8 consistency, docstrings, modular isolation of print routines to `main.py` freeing functional bounds to return structures natively. |
| **Exception Design** | Employs Python native `ValueError` across business boundaries ensuring robust cascading behavior while trapping IO operations effectively (e.g. `FileNotFoundError`). Never swallows. |

---

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
│   ├── accounts.csv        ← Account level info records
│   └── transactions.csv    ← Ledger entries mock dataset (25 rows)
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

## Running Tests

Verify the underlying systems using the built-in isolated unittests (Total: 39).
```powershell
python -m unittest discover -s tests -v
```

---

## Dataset Description

The `data/` folder comprises two CSV blocks utilized natively by `pandas`:
- **`transactions.csv`**: Contains a standard logging mock spanning 25 distinct transaction behaviors covering distinct users (`AccountNumber`, `TransactionType`, `Amount`, `Date`, etc).
- **`accounts.csv`**: Maps individual IDs against generic banking branch rules (`AccountType`, `Branch`) yielding a 5 row index utilized heavily when joining domains.

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
