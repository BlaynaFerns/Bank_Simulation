from datetime import datetime

class ATM:
    """Handles account operations and AI assistant logic."""

    def deposit(self, account: dict, amount: float):
        if amount <= 0:
            return "Amount must be positive."
        account["balance"] = account.get("balance", 0.0) + amount
        self.record_transaction(account, "Deposit", amount)
        return f"Deposited ₹{amount:.2f}. New balance: ₹{account['balance']:.2f}"

    def withdraw(self, account: dict, amount: float):
        if amount <= 0:
            return "Amount must be positive."
        if amount > account.get("balance", 0.0):
            return "Insufficient balance."
        account["balance"] -= amount
        self.record_transaction(account, "Withdrawal", amount)
        return f"Withdrew ₹{amount:.2f}. New balance: ₹{account['balance']:.2f}"

    def check_balance(self, account: dict):
        return f"Your balance is ₹{account.get('balance', 0.0):.2f}"

    def mini_statement(self, account: dict, size=5):
        txns = account.get("transactions", [])[-size:]
        if not txns:
            return "No transactions yet."
        lines = []
        for t in txns:
            lines.append(f"{t['timestamp']} | {t['type']:8} | ₹{t['amount']:.2f} | Bal: ₹{t['balance']:.2f}")
        return "\n".join(lines)

    def assistant(self, user_message: str):
        msg = (user_message or "").lower()
        if "balance" in msg:
            return "You can check your balance in the Balance section."
        elif "deposit" in msg:
            return "To deposit, go to Deposit section and enter an amount."
        elif "withdraw" in msg:
            return "To withdraw, go to Withdraw section and enter an amount."
        elif "transaction" in msg or "history" in msg:
            return "Check your mini statement under Transactions."
        else:
            return "I can help with deposits, withdrawals, balance, and transactions."

    def record_transaction(self, account: dict, txn_type: str, amount: float):
        account.setdefault("transactions", [])
        account["transactions"].append({
            "type": txn_type,
            "amount": amount,
            "balance": account["balance"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
