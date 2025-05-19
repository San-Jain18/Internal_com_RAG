import pandas as pd
from fuzzywuzzy import process
import streamlit as st

# Load the CSV file
#This consists of the full excel sheets folders too
df = pd.read_csv('Sharepoint MasterList_updated.csv')

df[['Lvl 3 Folder name','Lvl 2 Folder name']]=df[['Lvl 3 Folder name','Lvl 2 Folder name']].fillna("NaN")

# Convert columns to strings
for col in ['Lvl 1 Folder name', 'Lvl 2 Folder name', 'Lvl 3 Folder name']:
    df[col] = df[col].astype(str)

# Create a Path column
df['Path'] = df.apply(lambda row: '/'.join(filter(None, [row['Lvl 3 Folder name'], row['Lvl 2 Folder name'], row['Lvl 1 Folder name']])), axis=1)

# Function to search for keywords
def search_keywords(keyword, df):
    # Search in relevant columns
    matches = df[df.apply(lambda row: keyword.lower() in str(row['Topic']).lower() or
                                       keyword.lower() in str(row['Category']).lower() or
                                       keyword.lower() in str(row['Type']).lower() or
                                       keyword.lower() in str(row['Path']).lower(), axis=1)]
    
    # If no exact matches, use fuzzy matching
    if matches.empty:
        choices = df['Topic'].tolist() + df['Category'].tolist() + df['Type'].tolist() + df['Path'].tolist()
        best_match = process.extractOne(keyword, choices)
        if best_match and best_match[1] > 70:  # Threshold for fuzzy match
            matches = df[df.apply(lambda row: best_match[0].lower() in str(row['Topic']).lower() or
                                               best_match[0].lower() in str(row['Category']).lower() or
                                               best_match[0].lower() in str(row['Type']).lower() or
                                               best_match[0].lower() in str(row['Path']).lower(), axis=1)]
    
    return matches[['Topic', 'Category', 'Type', 'Path', 'Link']] if not matches.empty else None

# Streamlit UI
st.title("🔍 Training RAG Chatbot")

# Corrected input method
key_word = st.text_input("Type the keyword you want to search:")

if key_word:
    results = search_keywords(key_word, df)
    if results is not None:
        st.write("## Here are the best matches:")
        st.write(f"Found {len(results)} files or documents")
        st.table(results)
    else:
        st.write("⚠️ Oops! No file found.")
