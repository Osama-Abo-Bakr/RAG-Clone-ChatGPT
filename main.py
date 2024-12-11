import os
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def main():
    load_dotenv()

    st.set_page_config(page_title='Your Own ChatGPT',
                       page_icon='🤖', layout='wide')

    st.header('Your Own ChatGPT🤖')


    with st.sidebar:
        model = st.selectbox(label='Models', options=['gemma2-9b-it', 'llama-3.3-70b-versatile',
                                                      'llama-3.1-8b-instant', 'mixtral-8x7b-32768'])

        # Sidebar for Groq API key and link
        st.sidebar.title("Settings")
        api_key = st.sidebar.text_input("Enter your API Key:", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            if not os.getenv('GROQ_API_KEY'):
                st.error("Error: GROQ_API_KEY is not set. Please check your API key.")
            else:
                st.success("GROQ_API_KEY is set successfully.")

        # Steps to get the API key
        st.subheader("Steps to Get API Key:")
        st.markdown(
            """
            1. Sign in to Groq-Cloud: [Groq-Cloud](https://console.groq.com/keys)
            2. Create an API Key: [Groq-API](https://console.groq.com/keys)
            3. Copy the API key and paste it in the input area above.
            """
        )

    if model:
        llm = ChatGroq(
            model=model, temperature=0
        )

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content='You Are a helpful assistant.')
        ]


    user_input = st.chat_input('Your Message: ', key='user_input')

    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))

        with st.spinner('Thinking ...'):
            response = llm(st.session_state.messages)

        st.session_state.messages.append(AIMessage(content=response.content))

    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')







if __name__ == '__main__':
    main()