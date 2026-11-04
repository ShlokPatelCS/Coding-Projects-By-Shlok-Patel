"""Student Expense Tracker - a simple CSV-backed command-line application."""

import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["name", "amount", "category"]


def load_expenses():
    expenses = []
    if not DATA_FILE.exists():
        return expenses
    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                try:
                    amount = float(row["amount"])
                    if amount >= 0:
                        expenses.append({"name": row["name"], "amount": amount,
                                         "category": row["category"]})
                except (ValueError, KeyError, TypeError):
                    print("Warning: skipped an invalid saved expense.")
    except OSError as error:
        print(f"Could not read saved expenses: {error}")
    return expenses


def save_expenses(expenses):
    try:
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(expenses)
        return True
    except OSError as error:
        print(f"Could not save expenses: {error}")
        return False


def show_menu():
    print("\n===== STUDENT EXPENSE TRACKER =====")
    print("1. Add an Expense")
    print("2. View All Expenses")
    print("3. View Total Spending")
    print("4. View Spending by Category")
    print("5. Exit")


def add_expense(expenses):
    name = input("Expense name: ").strip()
    if not name:
        print("Expense name cannot be empty.")
        return
    try:
        amount = round(float(input("Amount ($): ")), 2)
    except ValueError:
        print("Please enter a valid number for the amount.")
        return
    if amount <= 0:
        print("Amount must be greater than zero.")
        return
    category = input("Category (e.g. Food, Transportation): ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    expenses.append({"name": name, "amount": amount, "category": category})
    if save_expenses(expenses):
        print("Expense added and saved successfully!")
    else:
        print("Expense added for this session, but could not be saved.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("\n--- All Expenses ---")
    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. {expense['name']} | ${expense['amount']:.2f} | {expense['category']}")


def view_total(expenses):
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal spending: ${total:.2f}")


def view_by_category(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    totals = {}
    for expense in expenses:
        category = expense["category"].strip().title()
        totals[category] = totals.get(category, 0) + expense["amount"]
    print("\n--- Spending by Category ---")
    for category in sorted(totals):
        print(f"{category}: ${totals[category]:.2f}")


def main():
    expenses = load_expenses()
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_total(expenses)
        elif choice == "4":
            view_by_category(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
