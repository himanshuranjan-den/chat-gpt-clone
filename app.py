import streamlit as st
from streamlit_chat import message
from langchain.llms.openai import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory
import os
# os.environ['OPENAI_API_KEY'] = ""
# llm = OpenAI(temperature=0.9, model_name="gpt-3.5-turbo-instruct")

if "conversation" not in st.session_state:
    st.session_state['conversation'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'API_KEY' not in st.session_state:
    st.session_state['API_KEY'] = ''

def getreponse(user_input, api_key):
    if st.session_state['conversation'] is None:
        llm = OpenAI(temperature=0.9, model_name="gpt-3.5-turbo-instruct",openai_api_key=api_key)
        st.session_state['conversation'] = ConversationChain(memory=ConversationSummaryMemory(llm=llm), llm=llm)
    response = st.session_state['conversation'].predict(input = user_input)
    return response


# setting up the UI for our page
st.set_page_config(page_icon=":robot:", page_title="Himanshu's GPT") 
st.markdown("<h1 style='text=-align: center;'>How can I help you buddy! </h1>",unsafe_allow_html=True)
st.sidebar.title(":cherry_blossom:")
st.session_state['API_KEY'] = st.sidebar.text_input("What is your API key!!", type="password")
summarise_button = st.sidebar.button("Summarise my conversation!!", key="summarise")
if summarise_button:
    summarise_placeholder = st.sidebar.write("Thanks my friend for chatting with me!. Here is the summary of our conversation")
    st.sidebar.write(st.session_state['conversation'].memory.buffer)

# This is for the response and question container

response_container = st.container()
# Now we have the container for the user input
container = st.container()

with container:
    with st.form(key="my_form",clear_on_submit=True):
        user_input = st.text_area("Your query goes here !!", key="input",height=100)
        submit_button = st.form_submit_button(label="Send")
        if submit_button:
            st.session_state['messages'].append(user_input)
            model_reponse = getreponse(user_input=user_input, api_key=st.session_state['API_KEY'])
            st.session_state['messages'].append(model_reponse)
            st.write(st.session_state['messages'])
            with response_container:
                # st.write(model_reponse)
                for i in range(len(st.session_state['messages'])):
                    if i%2 == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i)+'_user', avatar_style='croodles')
                    else:
                        message(st.session_state['messages'][i], is_user=False, key=str(i)+'_AI', avatar_style='bottts')

