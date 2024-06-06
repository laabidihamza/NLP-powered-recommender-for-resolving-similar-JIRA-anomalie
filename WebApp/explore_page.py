import streamlit as st
import pandas as pd

from wordcloud import WordCloud 
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objs as go
from collections import Counter,OrderedDict

def show_dashboard_page(supabase,name):
    st.subheader("Explore Dashboard")
    st.write('')

    res = supabase.table('users').select('*').execute()
    names = [entry["name"] for entry in res.data]
    
    roleres = supabase.table('users').select('role').eq('name',name).execute()
    role = roleres.data[0]['role']

    if role == 'admin':
        with st.container():
            with st.sidebar:
                selected_name = st.selectbox("Select a user",["All"] + names)
                st.write("")
                
            if selected_name == "All":
                # Retrieve summaries from the user_search table
                search_table_res = supabase.table("user_search").select("*").execute()
            else:
                search_user_id = supabase.table("users").select("user_id").eq("name",selected_name).execute().data[0]["user_id"]
                search_table_res = supabase.table("user_search").select("*").eq("user_id",search_user_id).execute()

            searches = search_table_res.data
            summaries = [entry["summary"] for entry in searches]
            descriptions = [entry["description"] for entry in searches]

            # Combine all summaries into a single string
            all_summaries = " ".join(summaries)
            all_descriptions = " ".join(descriptions)

            if len(all_summaries) == 0:
                st.warning('No data available for the selected user. Please select another user.')
            else:
                @st.experimental_fragment
                def create_wordcloud(text:str,title:str):
                    wordcloud = WordCloud(width=400, 
                                        height=200, 
                                        background_color ='white',
                                        ).generate(text)

                    fig, ax = plt.subplots(figsize=(10, 5))  
                    ax.imshow(wordcloud, interpolation="bilinear")  # Display the word cloud on the figure
                    ax.axis("off")

                    # Display the figure in Streamlit
                    st.pyplot(fig)
                    style = """
                    .e1nzilvr5 p{
                        text-align: center;
                    }
                    """
                    st.write(f"""
                            ***User {title} word cloud***
                            """)
                    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)


                col1, col2 = st.columns(2)
                with col1:
                    create_wordcloud(all_summaries,"summary")

                with col2:
                    create_wordcloud(all_descriptions,"description")
    else : 
        st.warning("You are not allowed to see wordcloud of other users.")

    search_table_res = supabase.table("user_search").select("*").execute()
    searches = search_table_res.data
    search_dates = [entry["search_date"] for entry in searches]

    report_table_res = supabase.table("user_report").select("*").execute()
    reports = report_table_res.data
    report_dates = [entry["report_date"] for entry in reports]
    ratings = [entry["rating"] for entry in reports]
                
    # Convert to pandas DataFrames for easier manipulation
    search_dates = pd.DataFrame(searches)
    report_dates = pd.DataFrame(reports)

    # Convert datestamps to datedate objects
    search_dates["search_date"] = pd.to_datetime(search_dates["search_date"])
    report_dates["report_date"] = pd.to_datetime(report_dates["report_date"])

    search_counts = search_dates.groupby(search_dates["search_date"].dt.date).size().reset_index(name="count")
    report_counts = report_dates.groupby(report_dates["report_date"].dt.date).size().reset_index(name="count")

    ratings_dict = OrderedDict([
        (1, "Bad"),
        (2, "Ok"),
        (3, "Medium"),
        (4, "Good"),
        (5, "Great")
    ])

    word_ratings = [ratings_dict[rating] for rating in ratings]

    emoticons_counts = Counter(word_ratings)

    # Create a pie chart with Plotly Express
    pie_chart = px.pie(
        data_frame=pd.DataFrame(emoticons_counts.items(), columns=["review", "count"]),
        names="review", 
        values = "count",
        title="Distribution of User Reviews",  
        hole=0.4,  
        )
    
    st.plotly_chart(pie_chart,use_container_width=True)


    if "radio_label_visibility" not in st.session_state:
        st.session_state["radio_label_visibility"] = "visible" 

    with st.sidebar:
        visualization_option = st.radio("Select Visualization",
                ["Both","Searches","Reports"],
                index=0, 
                horizontal=False,
                label_visibility = st.session_state["radio_label_visibility"],
                key="visualization_radio", 
        )
        st.write(" ")
        st.write('')
        st.write(" ")
        st.write(" ")
        st.write('')
        st.write(" ")
        st.write(" ")
        st.write('')
        st.write(" ")
        st.write('')
        # st.write(" ")
        if role == 'user':
            st.write(" ")
            st.write('')
            st.write(" ")
            st.write('')
            st.write(" ")

    if st.session_state.get('menu_option') != "Dashboard":
        st.session_state["radio_label_visibility"] = 'collapsed'
        with st.sidebar:
            st.write(" ")

    if visualization_option == "Both":
        fig = go.Figure()

        # Add stick plot for searches
        fig.add_trace(
            go.Scatter(
                x=search_counts["search_date"],
                y=search_counts["count"],
                mode='markers+lines',  # Both markers and lines for sticks
                name='Searches',
                line=dict(width=2, color='blue'),  # Stick appearance
                marker=dict(size=10),  # Marker appearance
            )
        )

        # Add stick plot for reports
        fig.add_trace(
            go.Scatter(
                x=report_counts["report_date"],
                y=report_counts["count"],
                mode='markers+lines',
                name='Reports',
                line=dict(width=2, color='red'),
                marker=dict(size=10)
            )
        )

        fig.update_layout(
            title="User Activity Over Time (Searches and Reports)",
            xaxis_title="Date",
            yaxis_title="Count",
            showlegend=True,
            legend=dict(x=0.01, y=0.99),  # Legend position
        )
        st.plotly_chart(fig,use_container_width=True)

    @st.cache_data
    def traffic_plot(graph_name: str, x_axe: list, y_axe: list, color: str):
        traffic_plot = go.Figure()

        traffic_plot.add_trace(
            go.Scatter(
                x=x_axe,
                y=y_axe,
                mode="markers+lines",
                name=graph_name,
                line=dict(width=2, color=color),
                marker=dict(size=10),
                showlegend=True
            )
        )

        traffic_plot.update_layout(
            title=f"User Traffic for '{graph_name}' Over Time",
            xaxis_title="Date",
            yaxis_title="Action Count",
            showlegend=True,
            legend=dict(x=0.01, y=0.99)
        )

        st.plotly_chart(traffic_plot,use_container_width=True)


    if visualization_option == "Searches":
        traffic_plot("Search", search_counts["search_date"],search_counts["count"], "blue")

    if visualization_option == "Reports":
        traffic_plot("Report", report_counts["report_date"],report_counts["count"], "red")
