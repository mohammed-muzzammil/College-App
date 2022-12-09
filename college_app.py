# A Fee Management System for a college using streamlit and python
#
#
import streamlit as st
import pandas as pd
import numpy as np
import os

# Headings

st.set_option('deprecation.showfileUploaderEncoding', False)

st.markdown("<h1 style='text-align: center; color: Light gray;'>Fee Management System</h1>", unsafe_allow_html=True)

# Enter the path here where all the temporary files will be stored
# For windows, use '\\' instead of '/'
# For linux or macOS, use '/'
temp = '/temp.csv'
temp_2 = '/temp_2.csv'

path = os.getcwd()
path = path + temp
path_2 = os.getcwd() + temp_2


# Function to update the csv file with the new data
def add_data(student_id, pending_fee, paid_fee, date, reciept_no, previous_paid_date):
    try:
        df = pd.read_csv(path)
        # Search for the student id in the csv file
        if student_id in df['Student id'].values:
            # Get the index of the student id
            index = df[df['Student id'] == student_id].index[0]
            # Update the pending fee
            df.loc[index, 'Balance Fee'] = pending_fee
            # Update the paid fee
            df.loc[index, 'FEES PAID'] = paid_fee
            # Update the date
            df.loc[index, 'Date'] = date
            # Update the reciept no
            df.loc[index, 'Reciept No'] = str(reciept_no)
            # Update the previous paid date
            df.loc[index, 'Previous Paid Date'] = previous_paid_date
            # Write the updated data to the csv file
            df.to_csv(path, index=False)
            st.success("Data Updated Successfully")
        else:
            st.error("Student id not found")
    except Exception as e:
        st.write("Oops!", str(e), "occurred.")


# Function to display the data
def display_data(student_id):
    try:
        df = pd.read_csv(path)
        # Search for the student id in the dataframe
        df = df[df['Student id'] == student_id]
        # Display the dataframe in a table format in the middle of the page
        st.table(df)

    except Exception as e:
        st.write("Oops!", str(e), "occurred.")


def file_upload():
    file = st.sidebar.file_uploader("Upload your file", type=["csv", "xlsx"])
    if st.sidebar.button("Upload"):
        if file and file.name.endswith("csv"):
            df = pd.read_csv(file)
            # Store the df in temp location
            df.to_csv(path)
        elif file and file.name.endswith("xlsx"):
            df = pd.read_excel(file)
            # Store the df in temp location
            df.to_csv(path)


# Function to search for the record of a student using student id as the key parameter in the csv file
def search_data(student_id):
    try:
        df = pd.read_csv(path)
        # Search for the student id in the dataframe
        df = df[df['Student id'] == student_id]
        # Display the dataframe in a table format in the middle of the page
        return df
    except Exception as e:
        st.write("Oops!", str(e), "occurred.")

# Upload the file
file_upload()
# Input Data
student_id = st.text_input("Enter Student ID")
student_name = None
student_year = None
student_branch = None
fee_fra = None
fee_mgt = None
paid_fee = None
date = None
pending_fee = None
previous_paid_date = None
reciept_no = None
if student_id:
    df = search_data(student_id)
    if df.empty:
        st.write("No data found")
    else:
        student_name = st.text_input("Student Name", df['NAME'].iloc[0])
        student_year = st.text_input("Student Year", df['year'].iloc[0])
        student_branch = st.text_input("Student Branch", df['Branch'].iloc[0])
        category = st.text_input("Category", df['Category'].iloc[0])
        fee_fra = st.text_input("Fee as per FRA", df['FRA FEE'].iloc[0])
        fee_mgt = st.text_input("College Fee as per Management", df['FEES'].iloc[0])
        previous_paid_amount = st.text_input("Previous Paid Amount", df['FEES PAID'].iloc[0])
        previous_paid_date = st.text_input("Previous Paid Date", df['Previous Paid Date'].iloc[0])
        col1, col2 = st.columns(2)
        with col2:
            st.warning("As on Date " + pd.datetime.now().strftime("%d/%m/%Y"))
        with col1:
            st.warning("Pending Fee: " + str(df['Balance Fee'].iloc[0]))

        paid_fee = st.text_input("Enter Paid Fee")
        reciept_no = st.text_input("Reciept No", df['Reciept No'].iloc[0])
        date = st.date_input("Enter Date", pd.to_datetime('today'))

# Add a Display Data button on the right side of the screen
if st.button("Add Data"):
    # Calculate the pending fee
    pending_fee = int(df['Balance Fee'].iloc[0]) - int(paid_fee)
    # Calculate the total paid fee
    paid_fee = int(previous_paid_amount) + int(paid_fee)
    # Add the pending fee, paid fee, date and reciept no to the csv file
    add_data(student_id, pending_fee, paid_fee, date, reciept_no, date)
    display_data(student_id)




