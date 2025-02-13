import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
import plotly.express as px

# Page Config
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Google Sheets Setup
def connect_to_google_sheets(json_keyfile, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(credentials)
    return client.open(sheet_name).sheet1

# Title
st.markdown("<h1 style='text-align: center;'>💸 Personal Expenses Tracker</h1>", unsafe_allow_html=True)
st.write("")
st.write("")
# Connect to Google Sheets
json_keyfile = r"C:\Users\nijap\Desktop\Sudhu\excel project\.streamlit\entry-form-449113-231fdbcd9e6c.json"
sheet_name = "Personal_Expense"
sheet = connect_to_google_sheets(json_keyfile, sheet_name)

# Fetch Data from Google Sheets & Convert to DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Convert 'Expense Date' column to datetime format
if not df.empty:
    df['Expense Date'] = pd.to_datetime(df['Expense Date'])

# Centered "Add Expense" Section (Not Full Width)

with st.container():
    col_expense,_,  col_delete = st.columns([3,0.3, 2])  # Centered effect
    with col_expense:
        st.markdown("<h3 style='text-align: center;'>➕ Add a New Expense</h3>", unsafe_allow_html=True)
        st.write("")  # Adds some spacing
        with st.form(key="expense_form"):
            expense_name = st.text_input("Expense Name*")
            category = st.selectbox("Category*", [" ", "🛒 Groceries", "🍽️ Food", "🚕 Transport", "🎭 Entertainment", "🏥 Healthcare ","🔌 Utilities","🛍️ Shopping", "❓Other"])
            amount = st.number_input("Amount*", min_value=0.0, format="%.2f")
            expense_date = st.date_input("Expense Date")
            notes = st.text_area("Notes (Optional)")
            submit_button = st.form_submit_button("Submit Expense")

    with col_delete:
        # Small & Centered "Delete Expenses" Section
        st.markdown("<h3 style='text-align: center;'>❌ Delete Expenses</h3>", unsafe_allow_html=True)
        st.write("")  # Adds some spacing
        st.write("")

        if not df.empty:
            expenses_to_delete = st.multiselect("Select expenses to delete", df['Expense Name'])

            if st.button("Delete Selected Expenses"):
                if expenses_to_delete:
                    for expense in expenses_to_delete:
                        row_index = df[df['Expense Name'] == expense].index[0]
                        sheet.delete_row(row_index + 2)  # Adjust for header row
                    st.success("🗑️ Selected expenses deleted successfully!")
                    st.rerun()
                else:
                    st.warning("No expenses selected.")
        else:
            st.warning("No expenses available to delete.")

if submit_button:
    if not expense_name or amount <= 0:
        st.warning("Please fill out all mandatory fields.")
    else:
        sheet.append_row([expense_name, category, amount, expense_date.strftime("%Y-%m-%d"), notes])
        st.success("Expense details submitted successfully!")
        st.rerun()  # Refresh the page after submitting
st.write("")
st.write("")
# Centered "Expense Summary" (Not Full Width)
st.markdown("<h3 style='text-align: center;'>📊 Expense Summary</h3>", unsafe_allow_html=True)

col1,col_summary, _ = st.columns([1 , 2, 1])  # Centered effect
with col_summary:
    date_filter = st.selectbox("Select Date Range", ["This Week", "This Month", "This Year", "Custom Range"])
    current_date = datetime.datetime.today()

# Calculate Total Expenses
def calculate_total(date_filter):
    if df.empty:
        return 0, pd.DataFrame()  # Return 0 if no data is present

    if date_filter == "This Week":
        start_date = current_date - datetime.timedelta(days=current_date.weekday())
    elif date_filter == "This Month":
        start_date = current_date.replace(day=1)
    elif date_filter == "This Year":
        start_date = current_date.replace(month=1, day=1)
    elif date_filter == "Custom Range":
        time_unit = st.radio("Select Time Unit", ["Days", "Weeks", "Months", "Years"])
        value = st.number_input(f"Enter number of {time_unit.lower()}", min_value=1, value=1)

        if time_unit == "Days":
            start_date = current_date - datetime.timedelta(days=value)
        elif time_unit == "Weeks":
            start_date = current_date - datetime.timedelta(weeks=value)
        elif time_unit == "Months":
            month = (current_date.month - value) % 12 or 12
            year = current_date.year - ((current_date.month - value - 1) // 12)
            start_date = current_date.replace(year=year, month=month, day=1)
        elif time_unit == "Years":
            start_date = current_date.replace(year=current_date.year - value, month=1, day=1)

    start_date = pd.to_datetime(start_date)
    filtered_data = df[df['Expense Date'] >= start_date]
    total_spent = filtered_data['Amount'].sum()
    return total_spent, filtered_data


# Show Expenses and Pie Chart in Two Columns
total_spent, filtered_data = calculate_total(date_filter)


_1, col_left,_2 , col_right,_3 = st.columns([0.3, 1.5, 0.5, 1, 0.5])# Expenses Table Left, Pie Chart Right

with col_left:
    st.write("")
    st.write("")
    if not filtered_data.empty:
        st.dataframe(filtered_data, height=250)
    else:
        st.warning("No expenses found in this period.")
# st.markdown(f"### 💰 Total Spent: **Rs.{total_spent:.2f}**")
st.markdown(f"<h4 style='text-align: center;'>💰 Total Spent: Rs. {total_spent:.2f}</h4>", unsafe_allow_html=True)


with col_right:
    if not filtered_data.empty:
        fig = px.pie(filtered_data, names='Category', values='Amount', title="Expense Breakdown", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

st.write("")
st.write("")
st.write("")
st.markdown("<h4 style='text-align: center; background: white; color:black;'>Made by Sudhanshu with ❤️</h4>", unsafe_allow_html=True)