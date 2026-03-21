import streamlit as st
import sqlite3
import pandas as pd

# Set up the Streamlit page configuration
st.set_page_config(page_title="Book Price Tracker", layout="wide")
st.title("📚 Live Book Price Dashboard")
st.write("This dashboard reads directly from our local SQLite database.")

# Fetch the data and connect it to the database
conn = sqlite3.connect('book_data.db')

# Use Pandas to run an SQL query and turn the results into a DataFrame
df = pd.read_sql_query("SELECT title, price FROM books", conn)
conn.close()

# Add a sidebar slider so the user can filter books by maximum price
max_price = st.sidebar.slider("Filter by Maximum Price (£)", 
                              min_value=0.0, 
                              max_value=float(df['price'].max()), 
                              value=60.0)

# Filter  data based on what the user selects on the slider
filtered_data = df[df['price'] <= max_price]

# Display the data (how many books are being tracked)
st.metric(label="Total Books Tracked", value=len(filtered_data))

# Make a bar chart to show the prices of the books
st.bar_chart(data=filtered_data, x='title', y='price')

# Show the raw data in a table format
st.write("### Raw Database Output")
st.dataframe(filtered_data)