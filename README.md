# 🏦 Bank Simulation- ATM Simulator with AI Assistant

## Overview
This project is a Python-based ATM simulator with an AI assistant.  
Users can create accounts, deposit and withdraw money, check balances, view transaction history, and interact with a simple AI assistant.  

---

## ✨ Features  

- **Account Management** – Create new accounts with unique account numbers and PIN  
- **Deposit & Withdraw** – Safely deposit or withdraw money  
- **Balance Check** – View current balance at any time  
- **Transaction History** – Keeps track of all deposits and withdrawals  
- **AI Assistant** – Ask questions about banking operations and get guidance  
- **Persistent Storage** – Data is saved in `accounts.json` and persists across sessions  
- **Streamlit GUI** – Easy-to-use web interface  

---

## 🛠️ Software Used

- **Python 3.10+**  
- **Streamlit** – Web interface  
- **JSON** – Data storage  
- **Requests** – Load Lottie animations for UI  
- **Lottie Files** – For animated UI elements  

## 📁 Folder Structure

```
atm_sim_ai/
├── accounts.json   # Stores account data and transactions
├── gui.py               # Streamlit GUI code
├── atm.py               # ATM class and logic
└── ai_assistant.py      # Simple AI assistant logic
├── README.md            # Project documentation
└── .gitignore           # Files to ignore in GitHub

```
---

## 💻 Code Breakdown

- **gui.py** – Main Streamlit interface, menu navigation, user login/logout, transaction handling  
- **atm.py** – Contains `ATM` class for deposit, withdraw, balance check, mini-statement, and AI assistant logic  
- **ai_assistant.py** – Handles basic AI responses for user queries  
- **accounts.json** – Stores account info, balances, and transaction history  

---

## 🖼️ Photos / UI Preview

![ATM GUI Screenshot](link-to-your-screenshot.png)  
*Example of the Streamlit interface with AI assistant*

---

## 📄 License

This project is intended for academic and demonstration purposes. It was originally created by YouTube. Feel free to use, modify, and expand upon it.
