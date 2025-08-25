import json
import os
from typing import Dict, Any
from datetime import datetime

def _ensure_data_file(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

def load_db(path: str) -> Dict[str, Any]:
    _ensure_data_file(path)
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_db(path: str, db: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def record_transaction(account: dict, ttype: str, amount: float, note: str = "") -> None:
    account.setdefault("transactions", [])
    account["transactions"].append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "type": ttype,
        "amount": round(amount, 2),
        "balance_after": round(account.get("balance", 0.0), 2),
        "note": note
    })