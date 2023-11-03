import sqlite3
from datetime import datetime

# Create a SQLite database and expenses table
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date DATE,
    category TEXT,
    description TEXT,
    amount REAL
)
""")
conn.commit()

def add_expense(date, category, description, amount):
    cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                   (date, category, description, amount))
    conn.commit()

def generate_monthly_report(year, month):
    cursor.execute("SELECT date, category, description, amount FROM expenses WHERE strftime('%Y-%m', date) = ?",
                   (f"{year}-{month:02d}",))
    expenses = cursor.fetchall()

    total = sum(expense[3] for expense in expenses)

    print(f"Monthly Report: {year}-{month:02d}")
    for expense in expenses:
        print(f"{expense[0]} - {expense[1]} - {expense[2]} - ${expense[3]:.2f}")
    print(f"Total Expenses: ${total:.2f}")

def main():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Generate Monthly Report")
        print("3. Exit")
        choice = input("Select an option (1/2/3): ")

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            description = input("Description: ")
            amount = float(input("Amount: $"))
            add_expense(date, category, description, amount)
            print("Expense added successfully.")

        elif choice == "2":
            year = int(input("Year (e.g., 2023): "))
            month = int(input("Month (1-12): "))
            generate_monthly_report(year, month)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
