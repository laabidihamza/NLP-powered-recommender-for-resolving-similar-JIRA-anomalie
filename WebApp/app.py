import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate

from urllib.parse import urlencode, urlparse, parse_qs

from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

# Set page title and icon
st.set_page_config(
    page_title="JIRA Solutions Recommender", page_icon="./assets/Vermeg-Logo.png", layout="centered", initial_sidebar_state="auto")

from home import home
from search_page import show_search_page
from explore_page import show_dashboard_page
from report import report

from upload_to_database import insert_user
from database import delete_user

# Hide the Streamlit menu
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""

# st.markdown(hide_menu, unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = None

data_path = "df_for_WebApp.pkl"

def load_data(data_path):
    st.session_state.data = pd.read_pickle(data_path)
load_data(data_path)

data = st.session_state.data

# Add logo
logo = st.image("./assets/Vermeg_logo.png", width=200)  

key = os.getenv('SUPABASE_KEY')
url = os.getenv('SUPABASE_URL')

supabase = create_client(url, key)

response = supabase.table('users').select("*").execute()
users = response.data

# Creating a dictionary for credentials
credentials = {
    'usernames': {}
}

# Populating the dictionary with user details
for user in users:
    email = user.get('email')
    username = user.get('username')
    name = user.get('name')
    password_hash = user.get('password')

    # Add user details to the credentials dictionary
    credentials['usernames'][username] = {
        'email': email,
        'name': name,
        'password': password_hash
    }

# Define cookie parameters (modify as needed)
cookie = {
    'name': "some_cookie_name",
    'key': "some_cookie_key",
    'expiry_days': 2
}

preauthorized = {
    'emails': ["abidihamza@vermeg.com"]  # Add pre-authorized emails if applicable
}

# Recreate the authenticator with corrected credentials
authenticator = Authenticate(
    credentials,
    cookie['name'],
    cookie['key'],
    cookie['expiry_days'],
    preauthorized
)

name, authentication_status, username = authenticator.login("main")

if authentication_status == None :
    st.info("Please login to access the app.")

if authentication_status == False: 
    st.error("Username/Password is incorrect. Please try again.")

if authentication_status == True:
    with st.sidebar:
        st.header(f"Welcome {name}  !")
        st.write(" ")
        st.write(" ")
        st.write(" ")

    # add selected to URL
    current_url = st.query_params
    menu_options = ["Home", "Search", "Dashboard", "Report"]
    default_index = menu_options.index(current_url.get("tab", "Home"))

    # Manual item selection
    if st.session_state.get('switch_button', False):
        st.session_state['menu_option'] = (st.session_state.get('menu_option', 0)+1) % 4
        manual_select = st.session_state['menu_option']
    else:
        manual_select = None

    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=["house", "search", "bar-chart-steps", "envelope"],
        menu_icon="cast",
        # default_index=default_index,
        default_index=0,
        orientation="horizontal",
        manual_select=manual_select, 
        key='menu_4',
            styles={
            "container": {"padding": "0!important"},
        },
    )
    # Update session state with the selected option
    st.session_state.menu_selection = selected

    if selected != menu_options[default_index]:
        current_url["tab"] = selected
        new_url = "?" + urlencode(current_url)

    if selected == "Home":
        home()
        st.button(f"Go to search"+"  "+"🡢", key='switch_button')
        st.session_state['menu_option'] = 0

    elif selected == "Search":
        show_search_page(data,supabase,username)

    elif selected == "Report":
        report(supabase,username)

    elif selected == "Dashboard":
        show_dashboard_page(supabase,name)
        
    else:
        st.write("Unknown selection")  

    with st.sidebar:
        if st.session_state.get('menu_selection') != "Dashboard":
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")

    with st.sidebar :
        res = supabase.table('users').select('role').eq('username',username).execute()
        role = res.data[0].get('role')
        res2 = supabase.table('users').select('name').execute()
        users = [entry["name"] for entry in res2.data]
        if role == 'admin':
            with st.popover("Manage Users"):
                action = st.radio("Select an action",["Add User","Delete User"],index=0,horizontal=True)
                if "action" not in st.session_state:
                    st.session_state.action = None
                with st.form(key='add_user', clear_on_submit=True,border=False):
                    st.session_state.action = action
                    if st.session_state.action == "Add User":
                        st.markdown("Enter user information")
                        name = st.text_input("Name")
                        username = st.text_input("Username")
                        email = st.text_input("Email")
                        password = st.text_input("Password",type='password')
                        role = st.radio("Role",["admin","user"],index=1)
                        if st.form_submit_button("Add User"):
                            if name and username and email and password:
                                if email.endswith("@vermeg.com"):
                                    insert_user(email, name, username, password,role)
                                    st.success("User added successfully")
                                else:
                                    st.error("Please enter a valid email address")
                            else:
                                st.error("Please fill all the fields")
                    else:
                        selected_name = st.selectbox("Select a name",users,index=None,placeholder="Select a user")
                        if st.form_submit_button("Delete User"):
                            if selected_name:
                                delete_user(selected_name)
                                st.success("User deleted successfully")
                            else:
                                st.error("Please fill all the fields")
        else:
            st.write(" ")
            st.write(" ")
            st.write(" ")
        authenticator.logout('Log out', 'main')
