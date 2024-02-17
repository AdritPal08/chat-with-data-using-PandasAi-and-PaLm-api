# Import the required modules
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai import SmartDatalake
from pandasai.llm import GooglePalm
import matplotlib.pyplot as plt
from pandasai import Agent
from dotenv import load_dotenv
import os

# Define a function to chat with a dataframe using pandasai
def chat_with_csv(dataframe, prompt):
    # Load the environment variables
    env_loaded = load_dotenv()
    # Get the Google API key
    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key = st.secrets["GOOGLE_API_KEY"]
    # Create a GooglePalm object for natural language processing
    llm = GooglePalm(api_key=api_key)
    # Create a SmartDataframe object from the dataframe
    pandas_ai = Agent(dataframe, config={"llm": llm, "cache": False})
    # Chat with the dataframe using the prompt
    result = pandas_ai.chat(prompt)
    # Return the result
    return result

# Define the main app function
def app(input_excel):
    # Display a header
    st.header("Chat With Data...")
    # Display some text
    st.write("Converse effortlessly with your data using simple and natural language in a seamless chat experience!")
    # Create a sidebar
    sidebar = st.sidebar
    # # Allow the user to upload multiple CSV files
    # input_csvs = sidebar.file_uploader(
    #     "Upload your file here!", type="csv", accept_multiple_files=True
    # )
    input_excel = input_excel
    # If the user uploaded some files
    if input_excel:
        # Let the user select a file from the uploaded files
        selected_file = sidebar.selectbox(
            "Select a excel file", [file.name for file in input_excel]
        )
        # Get the index of the selected file
        selected_index = [file.name for file in input_excel].index(selected_file)
        # Display a message on the sidebar
        sidebar.info("Excel file uploaded successfully")
        # Read the selected file as a dataframe
        data = pd.read_excel(input_excel[selected_index])            
        # data = pd.dataframe(data)
        # Create an expander to show the dataframe preview
        with st.expander("🔎 Data Preview"):
            # Display the first three rows of the dataframe
            st.dataframe(data)
        # Display a message
        st.info("Chat Below")
        # Initialize the session state for the messages
        if "messages" not in st.session_state:
            st.session_state.messages = []
        # Display the chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # Allow the user to enter a query
        input_text = st.chat_input("Enter the query")
        # If the user entered some text
        if input_text:
            # Append the user's query to the messages
            st.session_state.messages.append({"role": "user", "content": input_text})
            # Display the user's query
            with st.chat_message("user"):
                st.markdown(input_text)
            # Chat with the dataframe using the query
            result = chat_with_csv(data, input_text)
            # Get the figure numbers from matplotlib
            fig_number = plt.get_fignums()
            # If there are any figures
            if fig_number:
                # st.pyplot(plt.gcf())
                # Append the figure to the messages
                st.session_state.messages.append({"role": "assistant", "content": "Here is the plot:"})
                # Display the figure
                with st.chat_message("assistant"):
                    st.pyplot(plt.gcf())
            # Otherwise
            else:
                # Append the result to the messages
                st.session_state.messages.append({"role": "assistant", "content": result})
                # Display the result
                with st.chat_message("assistant"):
                    st.success(result)
