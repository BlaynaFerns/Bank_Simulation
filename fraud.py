from datetime import date
from typing import List
from config import DAILY_WITHDRAW_LIMIT

def _reset_daily_if_new_day(account: dict) -> None:
    today_str = date.today().isoformat()
    if account.get("last_withdraw_date") != today_str:
        account["last_withdraw_date"] = today_str
        account["daily_withdrawn"] = 0.0

def check_withdrawal_flags(account: dict, amount: float) -> List[str]:
    """Return warnings/flags, does not block by itself."""
    warnings = []
    _reset_daily_if_new_day(account)

    projected = float(account.get("daily_withdrawn", 0.0)) + amount
    if projected > DAILY_WITHDRAW_LIMIT:
        warnings.append(
            f"Daily withdrawal limit ({DAILY_WITHDRAW_LIMIT}) would be exceeded "
            f"by this withdrawal."
        )
    if amount >= 300:
        warnings.append("Unusually large withdrawal—please confirm this is intended.")
    return warnings

def register_withdrawal(account: dict, amount: float) -> None:
    _reset_daily_if_new_day(account)
    account["daily_withdrawn"] = float(account.get("daily_withdrawn", 0.0)) + amount

def failed_login(account: dict) -> int:
    account["failed_logins"] = int(account.get("failed_logins", 0)) + 1
    return account["failed_logins"]

def reset_failed_logins(account: dict) -> None:
    account["failed_logins"] = 0