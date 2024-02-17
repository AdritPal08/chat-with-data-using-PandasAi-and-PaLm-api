import streamlit as st
import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as stc


def app(input_excel):
    # st.set_page_config(page_title="about")
    st.header("Visualize Your Data...")
    st.write("Effortlessly visualize your data through drag-and-drop")
    sidebar = st.sidebar
    input_excel = input_excel
    if input_excel:
         selected_file = sidebar.selectbox(
            "Select a excel file", [file.name for file in input_excel])
         selected_index = [file.name for file in input_excel].index(selected_file)
         sidebar.info("Excel file uploaded successfully")
         data = pd.read_excel(input_excel[selected_index])
        #  st.info("Chat Below")
         # pyg_html = pyg.walk(data,return_html=True)
         pyg_html =pyg.walk(data, env='Streamlit', dark='dark',return_html=True)
        #  stc.html(pyg_html,scrolling=True,height=1000)
         stc.html(pyg_html,scrolling=True,width=1300, height=1000,)
         
         