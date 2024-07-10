import streamlit as st
import time
from openai import OpenAI

st._bottom
openai_api_key = st.text_input("OpenAI API Key", type="password")
assistant_id = st.text_input("Assistant ID")

# Set your OpenAI API key and assistant ID here
api_key = openai_api_key
assistant_id = assistant_id

if openai_api_key and assistant_id:
    st.write("OpenAI API Key and Assistant ID have been entered.")
    st.write(f"OpenAI API Key: {openai_api_key}")
    st.write(f"Assistant ID: {assistant_id}")

    # Set openAi client , assistant ai and assistant ai thread
    @st.cache_resource
    def load_openai_client_and_assistant():
        client = OpenAI(api_key=api_key)
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        thread = client.beta.threads.create()

        return client, my_assistant, thread

    client, my_assistant, assistant_thread = load_openai_client_and_assistant()

    # Check in loop if assistant ai parse our request
    def wait_on_run(run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    # Initiate assistant ai response
    def get_assistant_response(user_input=""):
        message = client.beta.threads.messages.create(
            thread_id=assistant_thread.id,
            role="user",
            content=user_input,
        )

        run = client.beta.threads.runs.create(
            thread_id=assistant_thread.id,
            assistant_id=assistant_id,
        )

        run = wait_on_run(run, assistant_thread)

        # Retrieve all the messages added after our last user message
        messages = client.beta.threads.messages.list(
            thread_id=assistant_thread.id, order="asc", after=message.id
        )

        return messages.data[0].content[0].text.value

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

    def submit():
        st.session_state.user_input = st.session_state.query
        st.session_state.query = ''

    st.title("FitEKG helfer")

    st.text_input("Play with me:", key='query', on_change=submit)

    user_input = st.session_state.user_input

    st.write("You entered: ", user_input)

    if user_input:
        result = get_assistant_response(user_input)
        st.header('Assistant :blue[cool] :pizza:', divider='rainbow')
        st.text(result)
else:
    st.write("Please enter both the OpenAI API Key and Assistant ID.")