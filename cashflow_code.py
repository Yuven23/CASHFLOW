import streamlit as st
import mysql.connector

# Function to connect to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="atm_database"
    )

# Function to check account balance
def check_balance(account_number):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Function to withdraw money
def withdraw_money(account_number, amount):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    balance = check_balance(account_number)
    if balance is not None and balance >= amount:
        new_balance = balance - amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
        conn.commit()
        cursor.close()
        conn.close()
        return new_balance
    else:
        cursor.close()
        conn.close()
        return None

# Function to deposit money
def deposit_money(account_number, amount):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    balance = check_balance(account_number)
    if balance is not None:
        new_balance = balance + amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
        conn.commit()
        cursor.close()
        conn.close()
        return new_balance
    else:
        cursor.close()
        conn.close()
        return None

# Streamlit UI
st.title('ATM Machine')

# Sidebar navigation
page = st.sidebar.radio("Navigation", ('Check Balance', 'Withdraw', 'Deposit'))

# Main content
if page == 'Check Balance':
    st.subheader('Check Balance')
    account_number = st.text_input("Enter account number:")
    if st.button('Check'):
        balance = check_balance(account_number)
        if balance is not None:
            st.write(f"Your account balance is: {balance}")
        else:
            st.write("Account not found or error occurred.")

elif page == 'Withdraw':
    st.subheader('Withdraw Money')
    account_number = st.text_input("Enter account number:")
    amount = st.number_input("Enter amount to withdraw:", min_value=0)
    if st.button('Withdraw'):
        new_balance = withdraw_money(account_number, amount)
        if new_balance is not None:
            st.write(f"Withdraw successful. Your new balance is: {new_balance}")
        else:
            st.write("Withdrawal failed. Insufficient balance or account not found.")

elif page == 'Deposit':
    st.subheader('Deposit Money')
    account_number = st.text_input("Enter account number:")
    amount = st.number_input("Enter amount to deposit:", min_value=0)
    if st.button('Deposit'):
        new_balance = deposit_money(account_number, amount)
        if new_balance is not None:
            st.write(f"Deposit successful. Your new balance is: {new_balance}")
        else:
            st.write("Deposit failed. Account not found.")

