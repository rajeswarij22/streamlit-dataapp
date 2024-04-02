import streamlit as st
import pandas as pd
import os
# Obtain the directory of the current script (__file__ is the path to the current script)
current_script_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the CSV file
csv_file_path = os.path.join(current_script_path, "Superstore_Sales_utf8.csv")
# Check if the file exists at the constructed path
if not os.path.exists(csv_file_path):
    st.error("CSV file not found at the specified path.")
else:
    # Display the App Title
    st.title("Data App Assignment")

#Load and Display Data
st.write("### Input Data and Examples")
# Use the constructed path to load the CSV file
df = pd.read_csv(csv_file_path, parse_dates=['Order_Date'])
st.dataframe(df)

# Using as_index=False here preserves the Category as a column.
category_sales = df.groupby("Category", as_index=False)["Sales"].sum()
st.bar_chart(category_sales, x="Category", y="Sales")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
sales_by_month = df.resample('M', on='Order_Date')['Sales'].sum()
st.line_chart(sales_by_month)

#st.write("## Your additions")
# (1) Add a drop down for Category
category = st.selectbox("Select a Category", df['Category'].unique())

# (2) Add a multi-select for Sub_Category in the selected Category (1)
sub_categories = df[df['Category'] == category]['Sub_Category'].unique()
selected_sub_categories = st.multiselect("Select Sub-Category", sub_categories)

# Initialize variables to avoid NameError
total_sales = 0
total_profit = 0
overall_profit_margin = 0

# (3) Show a line chart of sales for the selected items in (2)
if selected_sub_categories:
    mask = df['Sub_Category'].isin(selected_sub_categories)
    sales_by_month = df[mask].resample('M', on='Order_Date')['Sales'].sum()
    st.line_chart(sales_by_month)

    # (4) Calculate metrics only if sub-categories are selected
    selected_data = df[mask]
    total_sales = selected_data['Sales'].sum()
    total_profit = selected_data['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales else 0
    
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Overall Profit Margin", value=f"{overall_profit_margin:.2f}%")

# (5) Use the delta option in the overall profit margin metric
average_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100
profit_margin_delta = overall_profit_margin - average_profit_margin

st.metric(label="Profit Margin Delta",
          value=f"{overall_profit_margin:.2f}%",
          delta=f"{profit_margin_delta:.2f}% (from overall average)")
