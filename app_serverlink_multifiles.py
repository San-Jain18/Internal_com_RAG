#THIS CODE IS LINKED WITH THE SERVER FILEPATH CSV FILE
import pandas as pd
from fuzzywuzzy import process
import streamlit as st
import subprocess

# Load the CSV file
df = pd.read_csv('server_filepath_latest.csv')

# Function to search for keywords
def search_keywords(keyword, df):
    matches = df[df.apply(lambda row: keyword.lower() in str(row['Name']).lower(), axis=1)]
    
    if matches.empty:
        choices = df['Name'].tolist() 
        best_match = process.extractOne(keyword, choices)
        if best_match and best_match[1] > 70:
            matches = df[df.apply(lambda row: best_match[0].lower() in str(row['Name']).lower(), axis=1)]
    
    return matches[['Name', 'File_path']] if not matches.empty else None

def open_file(file_path):
    try:
        file_path = file_path.strip(' "')
        subprocess.run(['xdg-open', file_path], check=True)
        st.write(f"File opened: {file_path}")
    except subprocess.CalledProcessError as e:
        st.write(f"Error opening file: {e}")

# Streamlit UI
st.title("🔍 Training RAG Chatbot")

key_word = st.text_input("Type the keyword you want to search:")

if key_word:
    results = search_keywords(key_word, df)
    if results is not None:
        st.write("## Here are the best matches:")
        st.write(f"Found {len(results)} files or documents")
        
        for index, row in results.iterrows():
            col1, col2 = st.columns([3, 1])  # Creating two columns
            with col1:
                st.write(row['Name'])  # Display file name
            with col2:
                if st.button("Open File", key=index):
                    open_file(row['File_path'])
    else:
        st.write("⚠️ Oops! No file found.")
