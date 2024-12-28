import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from PIL import Image

# Set Page Configuration
st.set_page_config(page_title="Financial Management Assistant", page_icon="💰", layout="wide")

# Add Background Image
def add_background_image(image_path):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_path});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use a sample image URL (replace with your own hosted image)
add_background_image("https://via.placeholder.com/1920x1080.png?text=Background+Image")

# Application Title
st.title("💰 Financial Management Assistant")

# Sidebar with Icons
menu = {
    "🏠 Home": "Home",
    "📊 Track Expenses": "Track Expenses",
    "📈 Plan Budget": "Plan Budget",
    "🎯 Set Savings Goals": "Set Savings Goals",
    "📉 Stock Market Analysis": "Stock Market Analysis",
    "❓ Frequently Asked Questions": "Frequently Asked Questions"
}
choice = st.sidebar.radio("Menu", list(menu.keys()), format_func=lambda x: x.split(" ")[1])

# Data Storage
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

if "budget" not in st.session_state:
    st.session_state["budget"] = {}

if "savings_goals" not in st.session_state:
    st.session_state["savings_goals"] = {}

# Page Logic
if menu[choice] == "Home":
    st.subheader("Welcome to Your Financial Management Assistant")
    st.write("This app will help you manage your finances, track expenses, set budgets, and even give stock insights.")
    st.image("https://via.placeholder.com/600x400.png?text=Finance+Management")

elif menu[choice] == "Track Expenses":
    st.subheader("📊 Track Your Expenses")
    expense_date = st.date_input("Date")
    expense_category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Bills", "Others"])
    expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f")

    if st.button("Add Expense"):
        st.session_state["expenses"].append({"Date": expense_date, "Category": expense_category, "Amount": expense_amount})
        st.success("Expense added successfully!")

    if st.session_state["expenses"]:
        st.write("### All Expenses")
        df_expenses = pd.DataFrame(st.session_state["expenses"])
        st.dataframe(df_expenses)

        fig, ax = plt.subplots()
        df_expenses.groupby("Category")["Amount"].sum().plot(kind="bar", ax=ax, title="Expenses by Category")
        st.pyplot(fig)

elif menu[choice] == "Plan Budget":
    st.subheader("📈 Set Your Budget")
    budget_category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Bills", "Others"])
    budget_amount = st.number_input("Budget Amount", min_value=0.0, format="%.2f")

    if st.button("Set Budget"):
        st.session_state["budget"][budget_category] = budget_amount
        st.success(f"Budget for {budget_category} set to ${budget_amount:.2f}.")

    if st.session_state["budget"]:
        st.write("### Your Current Budgets")
        st.write(st.session_state["budget"])

elif menu[choice] == "Set Savings Goals":
    st.subheader("🎯 Set Your Savings Goals")
    goal_name = st.text_input("Goal Name")
    goal_amount = st.number_input("Goal Amount", min_value=0.0, format="%.2f")
    saved_amount = st.number_input("Amount Saved So Far", min_value=0.0, format="%.2f")

    if st.button("Save Goal"):
        st.session_state["savings_goals"][goal_name] = {"Goal": goal_amount, "Saved": saved_amount}
        st.success(f"Savings goal '{goal_name}' set successfully!")

    if st.session_state["savings_goals"]:
        st.write("### Your Savings Goals")
        for goal, values in st.session_state["savings_goals"].items():
            st.write(f"**{goal}**: Goal = ${values['Goal']:.2f}, Saved = ${values['Saved']:.2f}")

elif menu[choice] == "Stock Market Analysis":
    st.subheader("📉 Analyze Stocks")
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA):")

    if st.button("Get Stock Data"):
        if stock_symbol:
            try:
                stock_data = yf.Ticker(stock_symbol)
                hist = stock_data.history(period="1mo")
                st.write(f"### Stock Data for {stock_symbol.upper()}")
                st.line_chart(hist["Close"])
                st.write(hist.tail())
            except Exception as e:
                st.error(f"Error fetching stock data: {e}")
        else:
            st.warning("Please enter a valid stock symbol.")

elif menu[choice] == "Frequently Asked Questions":
    st.subheader("❓ Frequently Asked Questions")

    st.write("### How can I save money?")
    st.write("To save money, consider setting a budget, tracking your expenses, and prioritizing savings goals.")

    st.write("### What is the best way to invest?")
    st.write("Investing depends on your risk tolerance, time horizon, and financial goals. Diversification is key.")

    st.write("### How do I track my expenses?")
    st.write("You can track your expenses by categorizing them and regularly updating your spending in a budgeting tool or spreadsheet.")

    st.write("### What is a good savings goal?")
    st.write("A good savings goal should be specific, measurable, and achievable. For example, saving for an emergency fund, retirement, or a down payment on a house.")

    st.write("### How can I plan my budget?")
    st.write("A good budget should be based on your income and necessary expenses. Set realistic amounts for categories like rent, food, transportation, and savings.")
