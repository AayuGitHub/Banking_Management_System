# Banking Management System

A command-line application that simulates a basic bank — create accounts, deposit and withdraw money, transfer between accounts, and view a full statement with opening and closing balance, all saved to disk across sessions.

Built with Python as a learning project to practice working with multiple related object types, datetime serialization, and operations where the order of steps actually matters (you can't withdraw before you check the balance).

---

## What it does

You get a menu with 11 options when you run the app:

```
================================
 Banking Management System
================================
1.  Create Account
2.  View All Accounts
3.  Search Account
4.  Update Account
5.  Close Account
6.  Deposit Money
7.  Withdraw Money
8.  Transfer Money
9.  View Transaction History
10. View Account Statement
11. Exit
```

Each account belongs to a customer and holds their name, phone, email, account type (Saving or Current), current balance, and status (Active or Closed). Every deposit, withdrawal, and transfer is recorded as a transaction with a timestamp. Transfers get their own record too — showing which account sent money and which received it.

When you exit using option 11, all data is saved to three JSON files. The next run loads everything back automatically.

---

## How to run it

You just need Python 3 — no external libraries required.

```bash
python3 main.py
```

---

## Project structure

```
Banking_Management_System/
├── main.py               # Entry point — menu loop and all user input/output
├── Account.py            # Account class — represents one customer account
├── Transaction.py        # Transaction class — represents one deposit or withdrawal
├── Transfer.py           # Transfer class — represents one money transfer between accounts
├── BankManager.py        # All business logic — owns all three collections
├── accounts.json         # Auto-created on first save
├── transactions.json     # Auto-created on first save
└── transfers.json        # Auto-created on first save
```

### How the files relate to each other

- **`Account.py`** is the blueprint for a single customer account. It stores the customer's details and their current balance. The status starts as `"Inactive"` and becomes `"Active"` once created by the manager. Accounts can only be closed when the balance is zero.
- **`Transaction.py`** represents a single financial event — a deposit or a withdrawal. It stores the amount, type, timestamp, and a reference to the account it belongs to via `accountId`.
- **`Transfer.py`** represents a transfer between two accounts. When money is transferred, the manager creates one Transfer record (to track the movement) and two Transaction records — one withdrawal from the sender and one deposit for the receiver.
- **`BankManager.py`** owns all three lists and handles every operation — creating accounts, searching, updating, closing, deposits, withdrawals, transfers, statement generation, and JSON persistence.
- **`main.py`** never touches data directly. It collects input, calls the right method on `BankManager`, and prints whatever comes back.

---

## Features

- **Create account** — Enter customer name, phone, email, account type, and initial deposit. Account ID is generated automatically. Rejects duplicates if the same name and phone already exist.
- **View all accounts** — Lists every account alphabetically by customer name with full details.
- **Search account** — Find by Account ID or customer name. Either one works independently.
- **Update account** — Change name, phone, or email. Leave any field blank to skip it — blanks don't overwrite existing data.
- **Close account** — Only closes if the account balance is exactly zero and the status is Active. Blocked otherwise with a clear message.
- **Deposit money** — Enter Account ID and amount. Balance is updated and a Transaction record is created automatically.
- **Withdraw money** — Enter Account ID and amount. Checks that funds are available before deducting. Creates a Transaction record.
- **Transfer money** — Enter sender Account ID, receiver Account ID, and amount. Deducts from sender, adds to receiver, and creates one Transfer record plus two Transaction records (one per side).
- **View transaction history** — Lists every transaction across all accounts sorted by date and time.
- **Account statement** — Enter an Account ID to get a full statement: customer details, opening balance, closing balance, and every transaction on that account.
- **Persistent storage** — Three JSON files are written on exit and read on startup. UUIDs, datetimes, and all balances are fully preserved across sessions.

---

## What I learned building this

- Why **`datetime` objects can't be saved to JSON directly** — unlike plain strings or numbers, Python's `datetime` raises a `TypeError` when you try to serialize it. You have to call `.isoformat()` in `to_dict()` and `datetime.fromisoformat()` in `from_dict()` to convert both ways. The same issue applies to `uuid.uuid4()` — it returns a UUID object, not a string, so you need `str(uuid.uuid4())` or JSON will fail.
- What **opening balance and closing balance actually mean** — closing balance is what the account has right now. Opening balance is what it had before any of the current transactions: `opening = closing - total_credits + total_debits`. You work backwards from the current state.
- Why **a Transfer creates two Transactions** — the transfer record tracks the movement between accounts (from A to B), but the transaction records track each account's individual history (A lost money, B gained money). Without the two transactions, neither account's statement would be complete.
- The **keyword argument trap** — `search_account(accountId)` and `search_account(accountId=accountId)` look almost identical but do completely different things. The first passes the value as the first positional parameter (`customerName`), so every search silently returns `None`. The second passes it correctly by name.
- Why **`&` (bitwise AND) breaks boolean checks** — `balance == 0 & status == "Active"` doesn't compare both conditions. Python evaluates `0 & status` first (bitwise operation), which either crashes or gives a wrong result, before the comparisons even run. You always need `and` for combining conditions.
- How **one function can return different failure reasons** — `close_account` can fail because the account doesn't exist, or because the balance isn't zero, or because it's already closed. Returning different values lets the caller show a specific message instead of a generic "failed."
- That **`is not None` and `if value:` are not the same** — when updating an account, `if updatedName is not None:` lets an empty string through and erases the customer's name. `if updatedName:` treats both `None` and `""` as "user didn't enter anything, skip it" — which is what you actually want.
- The **three-file save and load pattern** — instead of three separate save functions and three separate load functions, you build a mapping of `(filename, class, list)` tuples and loop through once. One loop replaces six near-identical blocks of code.
