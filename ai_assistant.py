from textwrap import dedent

def ai_greet():
    return "Hello! 👋 I am your AI-powered ATM assistant. Type 'help' to see what I can do."


def respond(message: str, account: dict) -> str:
    """Very simple rule-based 'AI' tips engine for the CLI."""
    msg = (message or "").strip().lower()

    # Contextual tips
    balance = float(account.get("balance", 0.0))
    withdrawals_last5 = sum(1 for t in account.get("transactions", [])[-5:] if t["type"] == "withdraw")
    deposits_last5 = sum(1 for t in account.get("transactions", [])[-5:] if t["type"] == "deposit")

    if "help" in msg or "menu" in msg:
        return dedent("""
            I'm your ATM assistant. Try:
            - "what can i do"  → outline features
            - "saving tips"    → ideas to save more
            - "fees"           → explain common ATM fees
            - Or ask in plain English, e.g., "why was my withdrawal blocked?"
        """).strip()

    if "what can i do" in msg or "features" in msg:
        return dedent("""
            You can: check balance, deposit, withdraw, see mini statement, and get tips.
            I also warn you about large withdrawals or repeated failed logins.
        """).strip()

    if "fees" in msg:
        return dedent("""
            Common fees include out-of-network ATM charges and foreign transaction fees.
            Tip: Withdraw more per visit but less frequently to reduce total fees.
        """).strip()

    if "saving tips" in msg or "tips" in msg:
        tips = []
        if balance < 100:
            tips.append("Your balance is low—consider pausing non-essentials this week.")
        if withdrawals_last5 >= 3:
            tips.append("You've withdrawn often recently—try weekly budgeting envelopes.")
        if deposits_last5 == 0:
            tips.append("No recent deposits—consider setting up auto-deposit on payday.")
        if not tips:
            tips.append("You're doing fine! Consider moving a small, regular amount to savings.")
        return "\n".join(f"- {t}" for t in tips)

    if "blocked" in msg or "limit" in msg:
        return "Withdrawals can be limited per day for security. Try a smaller amount or wait until tomorrow."

    # Default helpful message
    return "Tell me what you need help with (try: 'saving tips', 'fees', or 'what can i do')."