# Bank Account Management & Transaction Analysis

> **Status: 🚧 Under Development — DataGrokr PLP Week 2 Mini-Project**

---

## Project Objective

This project will build a **Python-based Bank Account Management System** combined with a **pandas-powered Transaction Dataset Analysis** tool.

It demonstrates practical, real-world application of intermediate Python concepts taught in **DataGrokr Pre-Learning Program (PLP) Week 2**.

---

## DataGrokr PLP Week 2

This project is being developed as the **Week 2 mini-project** of the DataGrokr Pre-Learning Program.

It is built **phase by phase**, with each phase adding new features that correspond to the concepts covered in the weekly syllabus.

---

## Planned Features

> ⚠️ The features below are **planned / under development**. They are NOT yet implemented.

### Part A — OOP Bank Account System

- Account creation (account holder name, account number, initial balance)
- Deposit and withdrawal operations
- Balance management with validation
- Transaction history tracking
- Exception handling for invalid operations (e.g., overdraft, negative deposit)

### Part B — Dataset Analysis

- CSV transaction dataset (generated or imported)
- Reading and exploring data with **pandas**
- Filtering transactions by type, date, or amount
- Aggregation using `groupby()`
- Summary statistics (total deposits, total withdrawals, net balance)
- Joining datasets using `merge()`
- Numerical analysis using **NumPy**

### Python Concepts Demonstrated

> These concepts will be applied where they naturally fit — not forced artificially.

- Object-Oriented Programming (Classes, `__init__`, Inheritance, Polymorphism)
- List comprehensions and dictionary comprehensions
- `lambda`, `map()`, `filter()`
- Decorators
- Context managers
- Modules and packages
- Exception handling
- Clean, readable code

---

## Project Structure

```
Bank_Account/
│
├── README.md               ← This file
├── requirements.txt        ← Project dependencies
├── .gitignore              ← Files excluded from Git
│
├── src/                    ← All Python source code
│   ├── __init__.py
│   │
│   ├── models/             ← OOP classes and data models
│   │   ├── __init__.py
│   │   └── bank_account.py ← BankAccount class (planned)
│   │
│   ├── services/           ← Application/business logic
│   │   └── __init__.py
│   │
│   ├── analysis/           ← pandas/NumPy analysis scripts
│   │   └── __init__.py
│   │
│   └── main.py             ← Application entry point (planned)
│
├── data/                   ← CSV transaction datasets
│
└── tests/                  ← Unit and integration tests (planned)
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
| Phase 2 | BankAccount OOP implementation | 🔜 Planned |
| Phase 3 | pandas Transaction Analysis | 🔜 Planned |
| Phase 4 | Advanced features (decorators, context managers) | 🔜 Planned |
| Phase 5 | Testing & final cleanup | 🔜 Planned |

---

*DataGrokr Pre-Learning Program — Week 2 Mini-Project*
