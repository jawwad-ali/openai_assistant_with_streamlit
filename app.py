import streamlit as st
from model import OpenAIBot , MessageItem

st.set_page_config(
    page_title="Open AI Assistant API with Streamlit",
    page_icon=":speech_balloon:"
)

st.title("Your Senior Developer")
st.write("I will help you write your code more efficiently")

# Creating session
if "bot" not in st.session_state:
    st.session_state.bot = OpenAIBot("Senior Developer" , instructions="You are a Senior Developer. Write the code for me")

# Side bar and a button to remove chat history
with st.sidebar.success("Sidebar"):
    if st.button("Delete entire chat"):
        st.session_state.bot.delete_chat_history()

# Message
for m in st.session_state.bot.getMessages():
    with st.chat_message(m.role):
        st.markdown(m.content)

# Prompt functionality
if prompt := st.chat_input("Please ask a Question"):

    # Function to send message to the model
    st.session_state.bot.send_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt) 
    
    # if Message status is completed
    if(st.session_state.bot.isCompleted()):
        response: MessageItem = st.session_state.bot.get_latest_response()
        
        with st.chat_message(response.role):
            st.markdown(response.content)