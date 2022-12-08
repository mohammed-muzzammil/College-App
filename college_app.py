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


# Function to add data to the csv file
def add_data(student_id, student_name, student_year, student_branch, fee_fra, fee_mgt, paid_fee, date, pending_fee):
    try:
        # Create a dataframe
        df = pd.DataFrame({'Student ID': [student_id], 'Student Name': [student_name], 'Student Year': [student_year],
                           'Student Branch': [student_branch], 'Fee as per FRA': [fee_fra],
                           'Fee as per Management': [fee_mgt], 'Paid Fee': [paid_fee], 'Date': [date],
                           'Pending Fee': [pending_fee - int(paid_fee)]})
        # store the dataframe in a csv file append mode
        df.to_csv(path_2)
        st.write("Data added successfully")
        st.table(df)
    except Exception as e:
        st.write("Oops!", str(e), "occurred.")


# Function to display the data
def display_data(df):
    try:
        #df = pd.read_csv(path_2)
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
        df = df[df['Student ID'] == int(student_id)]
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
if student_id:
    df = search_data(student_id)
    if df.empty:
        st.write("No data found")
    else:
        student_name = st.text_input("Enter Student Name", df['Student Name'].iloc[0])
        student_year = st.selectbox("Enter Student Year", ("1st Year", "2nd Year", "3rd Year", "4th Year"), index=0)
        student_branch = st.selectbox("Enter Student Branch", ("CSE", "ECE", "EEE", "MECH", "CIVIL", "MBA"), index=0)
        fee_fra = st.text_input("Enter College Fee as per FRA", df['Fee as per FRA'].iloc[0])
        fee_mgt = st.text_input("Enter College Fee as per Management", df['Fee as per Management'].iloc[0])
        st.warning("Pending Fee: " + str(df['Pending Fee'].iloc[0]))
        paid_fee = st.text_input("Enter Paid Fee")
        date = st.date_input("Enter Date", pd.to_datetime('today'))

# Add a Display Data button on the right side of the screen
if st.button("Add Data"):
    add_data(student_id, student_name, student_year, student_branch, fee_fra, fee_mgt, paid_fee, date, df['Pending Fee'].iloc[0])
