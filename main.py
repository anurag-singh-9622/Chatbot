# import streamlit as st

# with st.chat_message()
# st.chat_input()

import streamlit as st
from openai import OpenAI

# messages = st.container(height=300)
# prompt = st.chat_input("Say something")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

with st.sidebar:
    # try:
    #     st.session_state.apikey = st.secrets["OPENAI_API_KEY"]
    # except:
    st.session_state.apikey = st.text_input('Enter Api Key')
    
    def reset_conversation():
        for key in st.session_state.keys():
            del st.session_state[key]
    st.button('Reset Chat', on_click=reset_conversation)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])



# User-provided prompt
if prompt := st.chat_input('say something here'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Function for generating LLM response
def generate_response(prompt_input = None, api_key=None):
    client = OpenAI(
    api_key = st.session_state.apikey,
    organization='org-CymJVeTtMPU7CBRWNjHzRaJt'
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # model = "gpt-4",
        messages=st.session_state.messages, # type: ignore
        max_tokens= 4000,
        temperature=1,
        top_p=0
    )
    response = completion.choices[0].message.content
    st.session_state.total_tokens += completion.usage.total_tokens

    return response

# Generate a new response if last message is not from assistant
try:
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response()
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
        with st.sidebar:
            st.session_state.total_tokens
except:
    st.error(f"Please Input API key")





# from openai import OpenAI
# import webbrowser
# client = OpenAI(
#     api_key= 'sk-proj-Dz0a4nHTI9JqU0jimgeRT3BlbkFJ1ZDpZE0SiqhEiDp81Dev',
#     organization='org-CymJVeTtMPU7CBRWNjHzRaJt'
#     )

# message = [
#       {"role": "system", "content": "You are a helpful assistant."},
#       {"role": "user", "content": "Hello!"}
#     ]
# content = ''
# total_tokens = 0
# total_input_tokens = 0
# total_output_tokens = 0
# while content != 'exit':
  
#   completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     # model = "gpt-4",
#     messages=message # type: ignore
#   )
#   response = completion.choices[0].message.content
#   tokens = completion.usage.total_tokens # type: ignore
#   input_tokens = completion.usage.prompt_tokens # type: ignore
#   output_tokens = completion.usage.completion_tokens # type: ignore
#   total_tokens += tokens
#   total_input_tokens += input_tokens
#   total_output_tokens += output_tokens
#   print(f'''{response} 
#         TOkens info:
#         input_token = {input_tokens} and output_tokens = {output_tokens} and token = {tokens} || 
#         total_input_tokes = {total_input_tokens} and total_output_tokens = {total_output_tokens} and total_tokens = {total_tokens}''')
#   content = input('Chat: ')
#   # print(message)
#   if content:
#     dict1 = {"role": 'assistant', "content": response}
#     message.append(dict1)
#     dict1 = {"role": 'user', "content": content}
#     message.append(dict1)
