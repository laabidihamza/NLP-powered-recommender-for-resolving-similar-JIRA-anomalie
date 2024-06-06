from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('SUPABASE_KEY')
url = os.getenv('SUPABASE_URL')

supabase = create_client(url, key)

def insert_user(username, name, password):
    # Hash the password
    # password_hash = hash_password(password)

    # Insert the new user into the database
    response = supabase.table("users").insert({
        "username": username,
        "name": name,
        "password": password
    }).execute()

    return response

# insert_user("test", "test", "test")

def fetch_user(username):

    response = supabase.table("users").select("*").eq("username", username).execute()

    user_data = response.data
    if user_data:
        print("User Information:")
        print(user_data)
    else:
        print("User not found.")
    return user_data    

def get_user(username):
    response = supabase.table("users").select("*").eq("username", username).execute()
    user_data = response.data
    if user_data:
        return user_data[0]
    else:
        return None
    
def update_user(username, name):
    response = supabase.table("users").update({
        "name": name
    }).eq("username", username).execute()
    return response

def delete_user(name):
    response = supabase.table("users").delete().eq("name", name).execute()
    return response


# fetch all users

response = supabase.table('users').select("*").execute()

users = response.data

print(users)

password_list = [user.get('password') for user in users]
print(password_list)