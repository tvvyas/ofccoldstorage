import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create inventory table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                name TEXT,
                gst_number TEXT,
                start_date TEXT,
                end_date TEXT,
                quantity INTEGER,
                rate_per_day REAL,
                bill_amount REAL
            )''')
conn.commit()

# Function to calculate bill amount
def calculate_bill(start_date, end_date, rate_per_day, quantity):
    days_stored = (end_date - start_date).days
    return days_stored * rate_per_day * quantity

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Add Item", "Update Item", "Delete Item", "View Items", "History"])

# Add Item Page
if page == "Add Item":
    st.title("Add Inventory Item")
    with st.form(key='add_item_form'):
        name = st.text_input("Name")
        gst_number = st.text_input("GST Number")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        quantity = st.number_input("Quantity", min_value=0)
        rate_per_day = st.number_input("Rate per Day", min_value=0.0)
        
        # Calculate bill amount
        if start_date and end_date:
            bill_amount = calculate_bill(start_date, end_date, rate_per_day, quantity)
        else:
            bill_amount = 0
        
        submit_button = st.form_submit_button(label='Add Item')
    
    if submit_button:
        c.execute('''INSERT INTO inventory (name, gst_number, start_date, end_date, quantity, rate_per_day, bill_amount)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, gst_number, start_date, end_date, quantity, rate_per_day, bill_amount))
        conn.commit()
        st.success("Item added successfully!")

# Update Item Page
elif page == "Update Item":
    st.title("Update Inventory Item")
    item_id = st.number_input("Enter the ID of the item to update", min_value=1)
    with st.form(key='update_item_form'):
        name = st.text_input("Name")
        gst_number = st.text_input("GST Number")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        quantity = st.number_input("Quantity", min_value=0)
        rate_per_day = st.number_input("Rate per Day", min_value=0.0)
        
        # Calculate bill amount
        if start_date and end_date:
            bill_amount = calculate_bill(start_date, end_date, rate_per_day, quantity)
        else:
            bill_amount = 0
        
        submit_button = st.form_submit_button(label='Update Item')
    
    if submit_button:
        c.execute('''UPDATE inventory SET 
                        name=?, gst_number=?, start_date=?, end_date=?, quantity=?, rate_per_day=?, bill_amount=?
                     WHERE id=?''', (name, gst_number, start_date, end_date, quantity, rate_per_day, bill_amount, item_id))
        conn.commit()
        st.success("Item updated successfully!")

# Delete Item Page
elif page == "Delete Item":
    st.title("Delete Inventory Item")
    item_id = st.number_input("Enter the ID of the item to delete", min_value=1)
    if st.button("Delete Item"):
        c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        st.success("Item deleted successfully!")

# View Items Page
elif page == "View Items":
    st.title("View Inventory Items")
    inventory_data = pd.read_sql_query("SELECT * FROM inventory", conn)
    st.dataframe(inventory_data)

# History Page
elif page == "History":
    st.title("Inventory History")
    history_data = pd.read_sql_query("SELECT * FROM inventory", conn)
    st.dataframe(history_data)

# Close the database connection
conn.close()
