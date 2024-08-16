import streamlit as st
import pandas as pd
import sqlite3
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
def calculate_bill(start_date, end_date, rate_per_day):
    days_stored = (end_date - start_date).days
    return days_stored * rate_per_day

# Title of the app
st.title("OFC Cold Storage System")

# Form to add or update inventory items
with st.form(key='inventory_form'):
    name = st.text_input("Name")
    gst_number = st.text_input("GST Number")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    quantity = st.number_input("Quantity", min_value=0)
    rate_per_day = st.number_input("Rate per Day", min_value=0.0)
    
    # Calculate bill amount
    if start_date and end_date:
        bill_amount = calculate_bill(start_date, end_date, rate_per_day)
    else:
        bill_amount = 0
    
    submit_button = st.form_submit_button(label='Add/Update Item')

# Add or update the inventory item
if submit_button:
    new_item = (name, gst_number, start_date, end_date, quantity, rate_per_day, bill_amount)
    
    # Check if the item already exists
    c.execute("SELECT * FROM inventory WHERE name=?", (name,))
    existing_item = c.fetchone()
    
    if existing_item:
        c.execute('''UPDATE inventory SET 
                        gst_number=?, start_date=?, end_date=?, quantity=?, rate_per_day=?, bill_amount=?
                     WHERE name=?''', (gst_number, start_date, end_date, quantity, rate_per_day, bill_amount, name))
        st.success("Item updated successfully!")
    else:
        c.execute('''INSERT INTO inventory (name, gst_number, start_date, end_date, quantity, rate_per_day, bill_amount)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', new_item)
        st.success("Item added successfully!")
    
    conn.commit()

# Display the inventory data
st.subheader("Inventory Data")
inventory_data = pd.read_sql_query("SELECT * FROM inventory", conn)
st.dataframe(inventory_data)

# Option to delete an item
delete_name = st.text_input("Enter the Name of the item to delete")
if st.button("Delete Item"):
    c.execute("DELETE FROM inventory WHERE name=?", (delete_name,))
    conn.commit()
    st.success("Item deleted successfully!")
    inventory_data = pd.read_sql_query("SELECT * FROM inventory", conn)
    st.dataframe(inventory_data)

# Close the database connection
conn.close()
