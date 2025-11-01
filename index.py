import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance 

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    @abstractmethod
    def withdraw(self, amount):
        pass

class SavingsAccount(Account):
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount > self.get_balance():
            raise ValueError("Insufficient funds.")
        self._Account__balance = self.get_balance() - amount


class CurrentAccount(Account):
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if self.get_balance() - amount < -500:
            raise ValueError("Overdraft limit reached (-₦500).")
        self._Account__balance = self.get_balance() - amount



class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💳 Bank App")
        self.root.geometry("420x420")
        self.root.config(bg="#f4f6f9")
        self.root.resizable(False, False)

       
        self.account_type = tk.StringVar(value="Savings")
        self.account = SavingsAccount("User", 0)

      
        header = tk.Label(
            root, text="🏦 Bank Account System", 
            font=("Segoe UI", 18, "bold"), 
            bg="#2d3436", fg="white", 
            pady=15
        )
        header.pack(fill=tk.X)

       
        frame = tk.Frame(root, bg="white", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.55, anchor="center", width=360, height=300)

      
        tk.Label(frame, text="Account Type:", font=("Segoe UI", 11, "bold"), bg="white").pack(pady=(10, 0))
        type_frame = tk.Frame(frame, bg="white")
        type_frame.pack(pady=5)
        tk.Radiobutton(type_frame, text="Savings", variable=self.account_type, value="Savings", command=self.change_account, bg="white", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Radiobutton(type_frame, text="Current", variable=self.account_type, value="Current", command=self.change_account, bg="white", font=("Segoe UI", 10)).pack(side="left", padx=10)

       
        self.balance_label = tk.Label(frame, text=f"Balance: ₦{self.account.get_balance():,.2f}", 
                                      font=("Segoe UI", 12, "bold"), bg="white", fg="#0984e3")
        self.balance_label.pack(pady=10)

     
        tk.Label(frame, text="Enter Amount:", font=("Segoe UI", 10), bg="white").pack()
        self.amount_entry = tk.Entry(frame, font=("Segoe UI", 11), relief="solid", justify="center")
        self.amount_entry.pack(pady=5, ipadx=5, ipady=3)

       
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=10)

        self.make_button(btn_frame, "Deposit", self.deposit_money, "#00b894", fg="black").pack(side="left", padx=8)
        self.make_button(btn_frame, "Withdraw", self.withdraw_money, "#d63031", fg="black").pack(side="left", padx=8)

      
        self.make_button(frame, "Exit", root.destroy, "#636e72", fg="red", width=15).pack(pady=10)

    def make_button(self, parent, text, command, color, fg="white", width=10):
        """Helper to create modern buttons."""
        btn = tk.Button(
            parent, text=text, command=command,
            bg=color, fg=fg,
            activebackground="#2d3436",
            relief="flat", cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            width=width, height=1
        )
       
        btn.bind("<Enter>", lambda e: btn.config(bg="#2d3436"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def change_account(self):
        if self.account_type.get() == "Savings":
            self.account = SavingsAccount("User", self.account.get_balance())
        else:
            self.account = CurrentAccount("User", self.account.get_balance())
        self.update_balance_label()

    def deposit_money(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.deposit(amount)
            self.update_balance_label()
            messagebox.showinfo("Deposit Successful", f"₦{amount:,.2f} deposited successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        self.amount_entry.delete(0, tk.END)

    def withdraw_money(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.withdraw(amount)
            self.update_balance_label()
            messagebox.showinfo("Withdrawal Successful", f"₦{amount:,.2f} withdrawn successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        self.amount_entry.delete(0, tk.END)

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ₦{self.account.get_balance():,.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
