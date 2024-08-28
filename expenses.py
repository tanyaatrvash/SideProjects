import tkinter as tk
import heapq

class Transaction:
    def __init__(self, date, description, category, amount):
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount

    def __str__(self):
        return f"{self.date}: {self.description} ({self.category}): ${self.amount}"

class FinanceTracker:
    def __init__(self):
        self.transactions = []  # List to store all transactions
        self.category_totals = {}  # Dictionary to store category totals
        self.transaction_history = []  # Queue to store transaction history
        self.min_max_heap = []  # Min-max-heap for tracking min and max amounts

    def add_transaction(self, date, description, category, amount):
        transaction = Transaction(date, description, category, amount)
        self.transactions.append(transaction)

        # Update category totals
        self.category_totals[category] = self.category_totals.get(category, 0) + amount

        # Update transaction history queue
        self.transaction_history.append(transaction)
        if len(self.transaction_history) > 10:  # Keep the last 10 transactions
            self.transaction_history.pop(0)

        # Update min-max-heap for tracking extremes
        heapq.heappush(self.min_max_heap, amount)
        if len(self.min_max_heap) > 10:  # Keep the last 10 amounts
            heapq.heappop(self.min_max_heap)

        # Update labels
        update_transaction_list_and_summary()

    def calculate_balance(self):
        expenses = 0
        income = 0
        for transaction in self.transactions:
            if transaction.amount < 0:
                expenses += transaction.amount
            else:
                income += transaction.amount
        return income, expenses

    def view_transactions(self):
        for transaction in self.transactions:
            print(f"{transaction.date}: {transaction.description} ({transaction.category}): ${transaction.amount}")

    def get_category_totals(self):
        return self.category_totals

    def get_transaction_history(self):
        return self.transaction_history

    def get_extremes(self):
        return heapq.nsmallest(1, self.min_max_heap), heapq.nlargest(1, self.min_max_heap)

def update_transaction_list_and_summary():
    # Clear listbox
    transaction_listbox.delete(0, tk.END)
    
    # Update the transaction list and calculate totals
    for transaction in tracker.transactions:
        transaction_listbox.insert(tk.END, str(transaction))

    # Income and expenses labels
    income, expenses = tracker.calculate_balance()
    income_label.config(text=f"Total Income: ${income:.2f}")
    expenses_label.config(text=f"Total Expenses: ${expenses:.2f}")

    # Category totals label
    category_totals = tracker.get_category_totals()
    category_totals_label.config(text=f"Category Totals: {category_totals}")

    # Transaction history label
    transaction_history = '\n'.join(map(str, tracker.get_transaction_history()))  # Join transaction strings
    transaction_history_label.config(text=f"Transaction History: {transaction_history}")

    # Extremes label
    min_amount, max_amount = tracker.get_extremes()
    extremes_label.config(text=f"Min Amount: ${min_amount[0]:.2f}, Max Amount: ${max_amount[0]:.2f}")



# Creating main application window
root = tk.Tk()
root.title("Personal Finance Tracker")


# GUI components 
label = tk.Label(root, text="Transactions:")
label.pack()

transaction_listbox = tk.Listbox(root)
transaction_listbox.pack()

def add_transaction():
    date = date_entry.get()
    description = description_entry.get()
    category = category_entry.get()
    amount = float(amount_entry.get())
    tracker.add_transaction(date, description, category, amount)
    update_transaction_list()
    clear_entry_fields()

def update_transaction_list():
    transaction_listbox.delete(0, tk.END)  # Clear listbox
    for transaction in tracker.transactions:
        transaction_listbox.insert(tk.END, f"{transaction.date}: {transaction.description} ({transaction.category}): ${transaction.amount}")
    # Income and expenses labels
    income, expenses = tracker.calculate_balance()
    income_label.config(text=f"Total Income: ${income}")
    expenses_label.config(text=f"Total Expenses: ${expenses}")

def clear_entry_fields():
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

date_label = tk.Label(root, text="Date:")
date_label.pack()
date_entry = tk.Entry(root)
date_entry.pack()

description_label = tk.Label(root, text="Description:")
description_label.pack()
description_entry = tk.Entry(root)
description_entry.pack()

category_label = tk.Label(root, text="Category:")
category_label.pack()
category_entry = tk.Entry(root)
category_entry.pack()

amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

add_button = tk.Button(root, text="Add Transaction", command=add_transaction)
add_button.pack()

income_label = tk.Label(root, text="Total Income: $0.00")
income_label.pack()

expenses_label = tk.Label(root, text="Total Expenses: $0.00")
expenses_label.pack()

# Category totals
category_totals_label = tk.Label(root, text="Category Totals: ")
category_totals_label.pack()

# Transaction history labels
transaction_history_label = tk.Label(root, text="Transaction History: ")
transaction_history_label.pack()

# Extremes labels
extremes_label = tk.Label(root, text="Min Amount: $0.00, Max Amount: $0.00")
extremes_label.pack()

# Sample usage:
tracker = FinanceTracker()

# Sample transactions
tracker.add_transaction("2023-10-20", "Groceries", "Food", -50.00)
tracker.add_transaction("2023-10-21", "Salary", "Income", 1000.00)
tracker.add_transaction("2023-10-22", "Gas", "Transportation", -30.00)

update_transaction_list_and_summary()

print("Finance Tracker - Transactions:")
tracker.view_transactions()

income, expenses = tracker.calculate_balance()
print(f"Total Income: ${income}")
print(f"Total Expenses: ${expenses}")

# Run the main application loop
root.mainloop()