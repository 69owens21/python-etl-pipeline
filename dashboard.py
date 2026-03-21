import streamlit as st
import sqlite3
import pandas as pd
from openai import OpenAI

#PAGE SETUP & SECURE API KEY INPUT
st.set_page_config(page_title="AI Data Pipeline", layout="wide")
st.title(" Live Book Price Dashboard & AI Assistant")

# Using sidebar for the API key so it stays source code
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# FETCH THE DATA
conn = sqlite3.connect('book_data.db')
df = pd.read_sql_query("SELECT title, price FROM books", conn)
conn.close()

# VISUALIZE THE RAW DATA
with st.expander(" View Raw Database & Charts"):
    st.bar_chart(data=df, x='title', y='price')
    st.dataframe(df)

#THE AI RETRIEVAL LAYER (RAG)
st.write("###  Chat with your Database")
st.write("Ask the AI questions about the scraped data! (e.g., 'What is the most expensive book?')")

# Initialize the chat history so it remembers the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#HANDLE USER INPUT
if user_question := st.chat_input("Ask a question about the books..."):
    # Show the user's question on the screen
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate the AI Response
    if not api_key:
        st.error(" Please enter your OpenAI API key in the sidebar to use the chat feature.")
    else:
        with st.chat_message("assistant"):
            client = OpenAI(api_key=api_key)
            
            #inject Pandas DataFrame directly into the AI's brain
            context_data = df.to_string(index=False)
            system_prompt = f"""
            You are a highly capable data analyst assistant. 
            Here is the latest pricing data extracted directly from our local database:
            
            {context_data}
            
            Answer the user's questions based ONLY on this provided data. Keep your answers concise.
            """
            
            # Make the API call
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                stream=True,
            )
            # Write the response to the screen as it streams in
            response = st.write_stream(stream)
        
        # Save the AI's response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})