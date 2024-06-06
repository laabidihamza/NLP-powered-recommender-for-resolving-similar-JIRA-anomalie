import streamlit as st
from streamlit_star_rating import st_star_rating

import time

def report(supabase,username):
    st.header("JIRA Solutions Recommender Report")

    response = supabase.table("users").select("*").eq("username", username).execute()
    user_data = response.data

    user_name = user_data[0]['name']
    user_id = user_data[0]['user_id']

    count_search_by_user_res = supabase.table("user_search") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    searches_by_user = len(count_search_by_user_res.data)

    response = supabase.table('user_report').select("rating").execute()
    average_rating = [rating['rating'] for rating in response.data]

    average = sum(average_rating)/len(average_rating)

    average_rating = round(average,1)

    @st.cache_data
    def get_usage_data(nb_search):
        usage_data = {
            "total_searches": nb_search,
            "average_user_rating": average_rating,
            "most_common_issue_types": ["API errors", "Configuration issues"]
        }
        return usage_data
    
    # usage_data = get_usage_data(searches_by_user)
    usage_data = get_usage_data(searches_by_user)

    # Set up a session state for the text input
    if "user_input" not in st.session_state:
        st.session_state.user_input = "" 

    st.write("This page provides insights into the usage of the JIRA Issue Resolution Assistant.")

    # Display usage data in a clear and informative way
    st.write(f"""
             **Total Searches:**  *{usage_data["total_searches"]}*
             """)
    st.write("**Average User Rating:**", f"  {usage_data['average_user_rating']} ⭐")
    st.write("**Most Common Issue Types:**")
    for issue_type in usage_data["most_common_issue_types"]:
        st.write(f"- {issue_type}")

    # Feedback section (optional)
    with st.container(border=True):
        rate = st_star_rating(
            label = "", 
            maxValue = 5, 
            defaultValue = 3, 
            key = "rating", 
            emoticons = True ,
            resetLabel="Reset"
        )
        feedback_text = st.text_area("Please share your feedback on this app:",value=st.session_state.user_input)

        submit_button = st.button("Submit Feedback")
    if submit_button:
        if feedback_text:

            response = supabase.table("user_report").insert({
                "user_id": user_id,
                "user_report": feedback_text,
                "rating": rate,
            }).execute()
            st.session_state.user_input = ""

            sucess_placeholder = st.empty()
            sucess_placeholder.success("Thank you for your feedback!")
            time.sleep(3)
            sucess_placeholder.empty()
        else:
            warning_placeholder = st.empty()
            warning_placeholder.warning("Please enter your feedback.")
            time.sleep(3)
            warning_placeholder.empty()

