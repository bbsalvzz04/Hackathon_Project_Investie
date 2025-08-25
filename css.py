import streamlit as st
import base64


def background_css(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()



def apply_BPIapp_background_css(encoded_image):
    # Background styling
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            background-color: black;
        }}
        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background: transparent;
        }}

        /* Popup styling */
        .popup-container {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px 24px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            z-index: 9998;
            max-width: 350px;
            width: 30%;
        }}
        .popup-container h2 {{
            font-size: 1.4rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 12px;
        }}
        .popup-container p {{
            font-size: 1rem;
            color: #555;
            margin-bottom: 20px;
        }}
        
        .btn-secondary {{
            display: inline-block;
            padding: 14px;
            border: 2px solid #ccc;
            border-radius: 8px;
            background: white;
            font-size: 1rem;
            color: #666;
            cursor: default;
            float:left;
            width: 120px;
            
            
            
        }}
        
        /* Streamlit button styling */
        div.stButton button {{
            background-color: #A21C20;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-size: 1rem;
            width: 120px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            position: fixed;
            top: 59.5%; 
            left: 56%;
            transform: translate(-50%, -50%);
            z-index: 9999;

        }}
        div.stButton button:hover {{
            background-color: #7E171A;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Render popup HTML
    st.markdown("""
    <div class="popup-container">
        <h2>Looks like you’re saving well.</h2>
        <p>Want to let your money start growing more?</p>
        <span class="btn-secondary">Not now</span>
    </div>
    """, unsafe_allow_html=True)

    # Render functional Start button (visually overlaid on popup)
    return st.button("Start", key="start_application")


def apply_BPIapp_background_css_nobtn(encoded_image):
    # Background styling
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            background-color: black;
        }}
        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background: transparent;
        }}
        </style>
    """, unsafe_allow_html=True)

def apply_background_with_chatbtn_css(encoded_image, blur=False):
    blur_style = "filter: blur(16px);" if blur else ""
    st.markdown(
        f"""
        <style>
        .custom-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            z-index: -1;
            {blur_style}
        }}
        .stApp {{
            background-color: transparent;
        }}
        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background: transparent;
        }}
        #chat-button {{
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 28px;
            cursor: pointer;
            z-index: 1001;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }}
        #chat-box {{
            position: fixed;
            bottom: 100px;
            right: 25px;
            width: 320px;
            max-height: 500px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            padding: 16px;
            z-index: 1000;
            overflow-y: auto;
        }}
        </style>
        <div class="custom-bg"></div>
        """,
        unsafe_allow_html=True
    )


def chatbot_button_css():
    st.markdown("""
    <style>
    /* Floating Button Container */
    div[data-testid="stButton"] {
        position: fixed;
        bottom: 30px;
        left: 30px;
        z-index: 9999;
    }

    /* Button styling (optional) */
    div[data-testid="stButton"] > button {
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        background-color: #A21C20;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

