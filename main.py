import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from deposit_rules import calculate_interest_rate, validate_term, calculate_compound_interest
import psutil

# Global variable to track the current state
current_state = "Withdrawal"  # Default state

# Check for running instances
def check_running_instance():
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python' and proc.info['pid'] != current_pid:
            try:
                cmdline = proc.cmdline()
                if len(cmdline) > 1 and 'main.py' in cmdline[1]:
                    proc.kill()
            except psutil.NoSuchProcess:
                continue

check_running_instance()

# Mapping product codes to names
products = {
    "5173/7": "Weekly Deposit",
    "104/2": "Monthly Deposit",
    "5071/5": "Daily Deposit"
}

# Combine product codes and names for display
product_dropdown_values = [f"{code} - {name}" for code, name in products.items()]

# Define input fields for clearing
input_fields = []

# Clear all input fields
def clear_inputs():
    for widget in input_fields:
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Checkbutton):
            widget.deselect()
    result_label.config(text="")

# Functions to switch between states
def toggle_mode():
    global current_state
    if current_state == "Withdrawal":
        current_state = "Deposit"
        update_ui_for_deposit()
    else:
        current_state = "Withdrawal"
        update_ui_for_withdrawal()

# Update UI for Withdrawal Simulation
def update_ui_for_withdrawal():
    clear_inputs()
    toggle_button.config(text="Switch to Deposit Mode")
    mode_label.config(text="Withdrawal Mode:")
    product_dropdown.grid_remove()
    term_label.grid_remove()
    entry_term_days.grid_remove()
    deposit_age_label.grid_remove()
    entry_deposit_age.grid_remove()
    principal_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
    entry_principal.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
    withdrawal_amount_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
    entry_withdrawal_amount.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
    weight1_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
    entry_weight1.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
    weight2_label.grid(row=4, column=0, pady=5, padx=5, sticky="w")
    entry_weight2.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
    tax_rate_label.grid(row=5, column=0, pady=5, padx=5, sticky="w")
    entry_tax_rate.grid(row=5, column=1, pady=5, padx=5, sticky="ew")
    full_withdrawal_button.grid(row=6, column=0, pady=5, padx=5)
    partial_withdrawal_button.grid(row=6, column=1, pady=5, padx=5)
    deposit_button.grid_remove()
    digital_bonus_checkbox.grid_remove()

# Update UI for Deposit Products Simulation
def update_ui_for_deposit():
    clear_inputs()
    toggle_button.config(text="Switch to Withdrawal Mode")
    mode_label.config(text="Deposit Mode:")
    product_dropdown.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
    term_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
    entry_term_days.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
    deposit_age_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
    entry_deposit_age.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
    principal_label.grid(row=4, column=0, pady=5, padx=5, sticky="w")
    entry_principal.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
    prime_rate_label.grid(row=5, column=0, pady=5, padx=5, sticky="w")
    entry_prime_rate.grid(row=5, column=1, pady=5, padx=5, sticky="ew")
    margin_rate_label.grid(row=6, column=0, pady=5, padx=5, sticky="w")
    entry_margin_rate.grid(row=6, column=1, pady=5, padx=5, sticky="ew")
    digital_bonus_checkbox.grid(row=7, column=0, columnspan=2, pady=5, sticky="n")
    deposit_button.grid(row=8, column=0, columnspan=2, pady=5)
    withdrawal_amount_label.grid_remove()
    entry_withdrawal_amount.grid_remove()
    weight1_label.grid_remove()
    entry_weight1.grid_remove()
    weight2_label.grid_remove()
    entry_weight2.grid_remove()
    tax_rate_label.grid_remove()
    entry_tax_rate.grid_remove()
    full_withdrawal_button.grid_remove()
    partial_withdrawal_button.grid_remove()

# Retrieve the product code from the selected value
def get_selected_product_code():
    selected_value = product_dropdown.get()
    if selected_value == "Select a Product":
        raise ValueError("Please select a product.")
    return selected_value.split(" - ")[0]

# Deposit Simulation
def calculate_deposit():
    try:
        product_code = get_selected_product_code()
        principal = float(entry_principal.get())
        term_days = int(entry_term_days.get())
        deposit_age = int(entry_deposit_age.get())
        prime_rate = float(entry_prime_rate.get())
        margin_rate = float(entry_margin_rate.get()) if entry_margin_rate.get() else 0
        digital_bonus = 0.1 if digital_bonus_var.get() else 0
        validate_term(product_code, term_days)
        if deposit_age > term_days or deposit_age < 2:
            raise ValueError("Deposit age must be between 2 and the term in days.")
        rate = calculate_interest_rate(product_code, principal, term_days, deposit_age, prime_rate + margin_rate, digital_bonus)
        result_label.config(
            text=f"Product: {products[product_code]} ({product_code})\n"
                 f"Interest Rate: {rate:.2f}%\n"
                 f"Accrued Interest: {rate:.2f} ₪"
        )
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Withdrawal Simulation
def calculate_full_withdrawal():
    try:
        withdrawal_amount = float(entry_withdrawal_amount.get())
        weight1 = float(entry_weight1.get())
        weight2 = float(entry_weight2.get())
        tax_rate = float(entry_tax_rate.get())
        result = withdrawal_amount * (1 - tax_rate / 100)
        result_label.config(text=f"Full Withdrawal Amount: {result:.2f} ₪")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def calculate_partial_withdrawal():
    try:
        withdrawal_amount = float(entry_withdrawal_amount.get())
        tax_rate = float(entry_tax_rate.get())
        result = withdrawal_amount * (1 - tax_rate / 100)
        result_label.config(text=f"Partial Withdrawal Amount: {result:.2f} ₪")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter GUI setup
root = tk.Tk()
root.title("Bank Simulator")
root.geometry("500x400")

# UI Elements
toggle_button = tk.Button(root, text="Switch to Deposit Mode", command=toggle_mode)
toggle_button.grid(row=0, column=0, pady=5)

mode_label = tk.Label(root, text="Mode:")
mode_label.grid(row=0, column=1)

product_dropdown = ttk.Combobox(root, values=product_dropdown_values, state="readonly")
product_dropdown.grid(row=1, column=1)

term_label = tk.Label(root, text="Term (in days):")
entry_term_days = tk.Entry(root)

deposit_age_label = tk.Label(root, text="Deposit Age (in days):")
entry_deposit_age = tk.Entry(root)

principal_label = tk.Label(root, text="Principal Amount:")
entry_principal = tk.Entry(root)

withdrawal_amount_label = tk.Label(root, text="Withdrawal Amount:")
entry_withdrawal_amount = tk.Entry(root)

weight1_label = tk.Label(root, text="Weight 1 (Principal):")
entry_weight1 = tk.Entry(root)

weight2_label = tk.Label(root, text="Weight 2 (Interest):")
entry_weight2 = tk.Entry(root)

tax_rate_label = tk.Label(root, text="Tax Rate:")
entry_tax_rate = tk.Entry(root)

prime_rate_label = tk.Label(root, text="Prime Rate (P):")
entry_prime_rate = tk.Entry(root)
entry_prime_rate.insert(0, "6.0")  # Default value

margin_rate_label = tk.Label(root, text="Margin Rate:")
entry_margin_rate = tk.Entry(root)

digital_bonus_var = tk.BooleanVar()
digital_bonus_checkbox = tk.Checkbutton(root, text="Digital Bonus (+0.10%)", variable=digital_bonus_var)

deposit_button = tk.Button(root, text="Calculate Deposit", command=calculate_deposit)
full_withdrawal_button = tk.Button(root, text="Full Withdrawal", command=calculate_full_withdrawal)
partial_withdrawal_button = tk.Button(root, text="Partial Withdrawal", command=calculate_partial_withdrawal)

result_label = tk.Label(root, text="")
result_label.grid(row=20, column=0, columnspan=2)

input_fields.extend([
    entry_term_days, entry_deposit_age, entry_principal,
    entry_withdrawal_amount, entry_weight1, entry_weight2,
    entry_tax_rate, entry_prime_rate, entry_margin_rate
])

# Initialize Withdrawal Mode
update_ui_for_withdrawal()

try:
    root.mainloop()
except Exception as e:
    print(f"Error: {e}")
finally:
    check_running_instance()
