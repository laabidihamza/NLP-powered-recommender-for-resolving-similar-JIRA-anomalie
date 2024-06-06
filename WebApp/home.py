import streamlit as st
import time 

def home(): 
    st.title("Welcome to our JIRA Solutions Recommender!")

    st.subheader("Find solutions for your JIRA problems quickly and efficiently.")

    intro = """
    This app leverages the power of Natural Language Processing (NLP) and the SBERT model to
    understand your JIRA issue descriptions and identify similar problems. It then helps you
    find potential solutions based on the retrieved information.

    **How it works:**

    1. Enter a concise summary of your JIRA issue.
    2. Provide a detailed description of the problem you're facing.
    3. Choose the similarity threshold.
    4. Click the "Search for Similar Issues" button.
    5. The app will use NLP and SBERT to find similar JIRA issues and present them to you.
    """
    def stream_data():
        for word in intro.split(" "):
            yield word + " "
            time.sleep(0.02)

    st.write_stream(stream_data)

    # hide_footer= """
    # <style>
    # footer{
    # visibility:visible;
    # footer:after{
    #     content:'Copyright @ 2021: Streamlit';
    #     display:block;
    #     position: relative;
    #     color: tomato:
    # }
    # </style>
    # """

    # st.markdown(hide_footer,unsafe_allow_html=True)
