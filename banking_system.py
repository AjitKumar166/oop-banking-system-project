"""
Simple Python Banking System
-----------------------------
Module 3 Project: OOP Basics (Classes, Encapsulation, Inheritance, Polymorphism)

Kept intentionally simple - built step by step from basic Python to OOP,
so each concept is easy to trace in the code.
"""

from datetime import datetime


# ---------------------------------------------------------------------------
# Transaction: a small class just to record history
# ---------------------------------------------------------------------------
class Transaction:
    def __init__(self, txn_type, amount):
        self.txn_type = txn_type
        self.amount = amount
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[{self.time}] {self.txn_type}: ₹{self.amount}"


# ---------------------------------------------------------------------------
# Account: base class (encapsulation lives here)
# ---------------------------------------------------------------------------
class Account:
    def __init__(self, acc_no, name, balance=0):
        self.acc_no = acc_no
        self.name = name
        self._balance = balance          # protected attribute (encapsulation)
        self.history = []                 # list of Transaction objects

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return
        self._balance += amount
        self.history.append(Transaction("Deposit", amount))
        print(f"✅ ₹{amount} deposited. New balance: ₹{self._balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
        elif amount > self._balance:
            print("❌ Insufficient balance.")
        else:
            self._balance -= amount
            self.history.append(Transaction("Withdraw", amount))
            print(f"✅ ₹{amount} withdrawn. New balance: ₹{self._balance}")

    def get_balance(self):
        return self._balance

    def show_history(self):
        print(f"\n--- Transaction History: {self.name} ({self.acc_no}) ---")
        if not self.history:
            print("No transactions yet.")
        for txn in self.history:
            print(txn)


# ---------------------------------------------------------------------------
# SavingsAccount: inheritance + polymorphism (overrides withdraw)
# ---------------------------------------------------------------------------
class SavingsAccount(Account):
    MIN_BALANCE = 500

    def withdraw(self, amount):
        if self.get_balance() - amount < self.MIN_BALANCE:
            print(f"❌ Savings account must keep minimum ₹{self.MIN_BALANCE}.")
        else:
            super().withdraw(amount)


# ---------------------------------------------------------------------------
# CurrentAccount: inheritance + polymorphism (own withdraw rule)
# ---------------------------------------------------------------------------
class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 1000

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
        elif amount > self.get_balance() + self.OVERDRAFT_LIMIT:
            print(f"❌ Exceeds overdraft limit of ₹{self.OVERDRAFT_LIMIT}.")
        else:
            self._balance -= amount
            self.history.append(Transaction("Withdraw", amount))
            print(f"✅ ₹{amount} withdrawn. New balance: ₹{self._balance}")


# ---------------------------------------------------------------------------
# Bank: manages all accounts
# ---------------------------------------------------------------------------
class Bank:
    def __init__(self):
        self.accounts = {}   # acc_no -> Account object
        self.next_id = 1001

    def create_account(self, name, acc_type, initial_deposit=0):
        acc_no = str(self.next_id)
        self.next_id += 1

        if acc_type == "2":
            account = CurrentAccount(acc_no, name, initial_deposit)
        else:
            account = SavingsAccount(acc_no, name, initial_deposit)

        self.accounts[acc_no] = account
        print(f"✅ Account created! Account No: {acc_no}")
        return acc_no

    def get_account(self, acc_no):
        account = self.accounts.get(acc_no)
        if not account:
            print("❌ Account not found.")
        return account


# ---------------------------------------------------------------------------
# Menu-driven interface
# ---------------------------------------------------------------------------
def main():
    bank = Bank()

    while True:
        print("\n===== Simple Banking System =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        try:
            if choice == "1":
                name = input("Enter name: ").strip()
                acc_type = input("Account type (1=Savings, 2=Current): ").strip()
                deposit = float(input("Initial deposit: ").strip() or 0)
                bank.create_account(name, acc_type, deposit)

            elif choice == "2":
                acc = bank.get_account(input("Enter account number: ").strip())
                if acc:
                    acc.deposit(float(input("Amount to deposit: ")))

            elif choice == "3":
                acc = bank.get_account(input("Enter account number: ").strip())
                if acc:
                    acc.withdraw(float(input("Amount to withdraw: ")))

            elif choice == "4":
                acc = bank.get_account(input("Enter account number: ").strip())
                if acc:
                    print(f"Balance: ₹{acc.get_balance()}")

            elif choice == "5":
                acc = bank.get_account(input("Enter account number: ").strip())
                if acc:
                    acc.show_history()

            elif choice == "6":
                print("Goodbye! 👋")
                break

            else:
                print("❌ Invalid choice.")

        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
