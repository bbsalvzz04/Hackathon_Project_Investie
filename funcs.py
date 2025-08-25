import streamlit as st
import base64
import pandas as pd
from css import apply_background_with_chatbtn_css
import altair as alt




def toggle_chat():
    st.session_state.show_chat = not st.session_state.show_chat

def get_encoded_bg(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    

def login():
    df = pd.read_csv("clients2.csv")
    st.title("🔑 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if username in df["Username"].values:
            st.session_state.logged_in = True
            st.session_state.username = username
            return username
        else:
            st.error("Invalid username or password.")


def find_customer(username):
    df = pd.read_csv("clients2.csv")
    match = df[df["Username"] == username]

    if match.empty:
        return "No customer data found."
    

    return ", ".join([f"{col}: {val}" for col, val in match.iloc[0].items()])

def display_tracker(data):  
    bg_img = get_encoded_bg("BPIhome_investor.png")


    apply_background_with_chatbtn_css(bg_img)

    principal = data['Principal']
    portfolio_value = data['Portfolio_Value']
    gain = portfolio_value - principal


    # Prepare data for horizontal bar chart
    chart_data = pd.DataFrame({
        "Type": ["Principal", "Portfolio Value"],
        "Amount": [principal, portfolio_value]
    })
    chart = alt.Chart(chart_data).mark_bar().encode(
            x='Amount:Q',
            y=alt.Y('Type:N', sort=None),
            color='Type:N'
        )
    for _ in range(23):
        st.text("")

    if st.session_state.view_tracker:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.altair_chart(chart, use_container_width=False)

    
