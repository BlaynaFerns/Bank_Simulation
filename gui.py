import streamlit as st
import json
import os
from datetime import datetime
from streamlit_lottie import st_lottie
import requests
from atm import ATM  # <-- import your ATM class

# -----------------------------
# File paths
# -----------------------------
DATA_DIR = r"D:\Blayna College\PROJECTS\atm_sim_ai\data"
os.makedirs(DATA_DIR, exist_ok=True)
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")

# -----------------------------
# Load/Save accounts (UTF-8)
# -----------------------------
def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Fix corrupted or empty file
        data = {}
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data


def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=4, ensure_ascii=False)

# -----------------------------
# Transaction recording
# -----------------------------
def record_transaction(account_number, transaction_type, amount):
    accounts = load_accounts()
    acc = accounts[account_number]
    acc.setdefault("transactions", [])
    acc["transactions"].append({
        "type": transaction_type,
        "amount": amount,
        "balance": acc.get("balance", 0.0),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_accounts(accounts)
    st.session_state.accounts = accounts

# -----------------------------
# Assistant history
# -----------------------------
def append_assistant_history(account_number, user_input, response):
    accounts = load_accounts()
    acc = accounts[account_number]
    acc.setdefault("assistant_history", [])
    acc["assistant_history"].append({
        "user": user_input,
        "assistant": response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_accounts(accounts)
    st.session_state.accounts = accounts

# -----------------------------
# Lottie loader
# -----------------------------
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# -----------------------------
# Initialize session state
# -----------------------------
if "accounts" not in st.session_state:
    st.session_state.accounts = load_accounts()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = None

atm = ATM()  # ATM object

# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="BANK OF BM", page_icon="🏦", layout="wide")
st.title("🏦 BANK OF BM")

# -----------------------------
# Sidebar Menu
# -----------------------------
menu = ["Home", "Create Account", "Login", "Deposit", "Withdraw", "Balance", "Transactions", "Assistant", "Logout", "Exit"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Pages
# -----------------------------
if choice == "Home":
    st.subheader("Welcome to BANK OF BM")
    st.write("Use the sidebar to navigate through options.")
    lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=300)

elif choice == "Create Account":
    st.subheader("Create New Account")
    new_account = st.text_input("Enter account number")
    pin = st.text_input("Set PIN", type="password")

    if st.button("Create"):
        accounts = load_accounts()
        if new_account in accounts:
            st.error("Account already exists!")
        else:
            accounts[new_account] = {
                "pin": pin,
                "balance": 0.0,
                "transactions": [],
                "assistant_history": []
            }
            save_accounts(accounts)
            st.session_state.accounts = accounts
            st.success("Account created successfully!")

elif choice == "Login":
    st.subheader("Login")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        accounts = load_accounts()
        st.session_state.accounts = accounts
        if acc in accounts and accounts[acc]["pin"] == pin:
            st.session_state.logged_in = acc
            st.success("Login successful!")
        else:
            st.error("Invalid credentials!")

elif choice == "Deposit":
    if st.session_state.logged_in:
        acc = st.session_state.logged_in
        amount = st.number_input("Enter amount to deposit", min_value=0.0)
        if st.button("Deposit"):
            accounts = load_accounts()
            response = atm.deposit(accounts[acc], amount)
            save_accounts(accounts)
            st.session_state.accounts = accounts
            record_transaction(acc, "Deposit", amount)
            st.success(response)
    else:
        st.warning("Please login first!")

elif choice == "Withdraw":
    if st.session_state.logged_in:
        acc = st.session_state.logged_in
        amount = st.number_input("Enter amount to withdraw", min_value=0.0)
        if st.button("Withdraw"):
            accounts = load_accounts()
            response = atm.withdraw(accounts[acc], amount)
            save_accounts(accounts)
            st.session_state.accounts = accounts
            record_transaction(acc, "Withdrawal", amount)
            if "Insufficient" in response:
                st.error(response)
            else:
                st.success(response)
    else:
        st.warning("Please login first!")

elif choice == "Balance":
    if st.session_state.logged_in:
        acc = st.session_state.logged_in
        accounts = load_accounts()
        response = atm.check_balance(accounts[acc])
        st.info(response)
    else:
        st.warning("Please login first!")

elif choice == "Transactions":
    if st.session_state.logged_in:
        acc = st.session_state.logged_in
        accounts = load_accounts()
        st.write("Transaction History")
        st.json(accounts[acc]["transactions"])
    else:
        st.warning("Please login first!")

elif choice == "Assistant":
    if st.session_state.logged_in:
        acc = st.session_state.logged_in
        st.subheader("AI Assistant")
        user_input = st.text_input("Ask me anything:")
        if st.button("Ask"):
            if user_input.strip():
                response = atm.assistant(user_input)
                st.write("**Assistant:**", response)
                append_assistant_history(acc, user_input, response)

        st.write("**Conversation History**")
        accounts = load_accounts()
        for entry in accounts[acc]["assistant_history"]:
            st.write(f"**You:** {entry['user']}")
            st.write(f"**Assistant:** {entry['assistant']}")
    else:
        st.warning("Please login first!")

elif choice == "Logout":
    if st.session_state.logged_in:
        st.session_state.logged_in = None
        st.success("Logged out successfully!")
    else:
        st.info("You are not logged in.")

elif choice == "Exit":
    st.warning("Close the browser tab to exit the application.")
