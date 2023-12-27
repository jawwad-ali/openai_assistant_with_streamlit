import streamlit as st
from model import OpenAIBot , MessageItem

import os
import shutil

st.set_page_config(
    page_title="Open AI Assistant API with Streamlit",
    page_icon=":speech_balloon:"
)

st.title("Your PDF Analyzer") 
st.write("I will answer your query based on your attached PDF")

# # function to bring the selected file to project directory
def move_file_to_directory(uploaded_file, destination_directory):
    # Check if the destination directory exists, if not, create it
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Save the uploaded file to a temporary location on the server
    temp_file_path = os.path.join(destination_directory, uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())

    # Create the full destination path by joining the destination directory and filename
    destination_path = os.path.join(destination_directory, uploaded_file.name)

    # Move the file to the destination directory
    shutil.move(temp_file_path, destination_path)
    st.write("File moved successfully!")

# # Directory where file is stored
destination_folder = "temp" 

# ########################## ############### STREAMLIT UI # ########################## ############


uploaded_file = st.file_uploader("Upload your PDF")
# # Check if a file has been uploaded 
if uploaded_file is not None:
    # Move the uploaded file to the destination directory
    destination_path = move_file_to_directory(uploaded_file, destination_folder)
    st.write(uploaded_file) 

    if "assistant_bot" not in st.session_state:
        if uploaded_file is not None:
            st.session_state.assistant_bot = OpenAIBot("PDF ANALYZER" , instructions="answer your query based on your attached PDF", fileFromUI = uploaded_file.name)  

        st.write(st.session_state.assistant_bot)

    # Message
    for m in st.session_state.assistant_bot.getMessages():
        with st.chat_message(m.role):
            st.markdown(m.content)

    #Prompt functionality
if prompt := st.chat_input("Please ask a Question"):

    # Function to send message to the model
    st.session_state.assistant_bot.send_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt) 

        # if Message status is completed
        if st.session_state.assistant_bot.isCompleted():
            response: MessageItem = st.session_state.assistant_bot.get_latest_response()
                
    with st.chat_message(response.role):
        st.markdown(response.content)

# # Side bar and a button to remove chat history
with st.sidebar.success("Sidebar"):
    if st.button("Delete entire chat"):
        st.session_state.assistant_bot.delete_chat_history()

# Example Prompts
# What is in the fifth chapter of the book. explain in 50 words
# Name all the chapters of the book