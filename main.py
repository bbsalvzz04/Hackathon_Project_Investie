import streamlit as st
import pandas as pd

from css import apply_background_with_chatbtn_css, chatbot_button_css, apply_BPIapp_background_css
from funcs import toggle_chat, get_encoded_bg, login, find_customer, display_tracker


from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor   

# ------------------ Client Filtering for Nudging ------------------
df = pd.read_csv("clients2.csv")
non_investors = df[df["Investor"]=="No"]



# -------------------- gpt setup ------------------
load_dotenv()
class AgentResponse(BaseModel):
    topic: str
    summary: str 
    sources: list[str]
    tools_used: list[str]

#df = pd.read_csv("clients.csv")         #read CSV 
llm = ChatOpenAI(model="gpt-4.1-mini")          #loading llm 
parser = PydanticOutputParser(pydantic_object=AgentResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", # info tells the llm what to do
            
            """
            You are a financial assistant guiding customers through their first BPI investment. 
            Respond to queries using the necessary tools.
            - for personal advice, use provided customer details {customer_info_str}
            - For general informational questions, use internet search
                and wrap the output in this format and provide no other text\n{format_instructions}
            
            Do not instruct users to consult a financial advisor. Instead, emphasize that you 
            are a helpful guide providing general information and insights about BPI investments. 
            Present your responses as suggestions, explanations, or educational guidance—never as professional, 
            personalized financial advice. Encourage learning and informed decision-making rather than authoritative 
            prescriptions.

            Be polite, respectful, but most of all encouraging. 
            Match the language that they use, whether Filipino or English, or a mix of both.
            Any questions outside of BPI investments or financing, provide no information.

            """,
        ),

        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]

).partial(format_instructions=parser.get_format_instructions)

prompt2 = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            """
            You are a financial coach giving short, proactive nudges to customers.  
            Address them by their Username.
            Your response should be at most 1-2 sentences.  
                - If the customer is on track, congratulate them and encourage consistency.  
                - If the customer shows risky or concerning behavior, give a gentle heads-up and a simple suggestion.  
            Always be clear, supportive, and motivating.
            Here are the customer's details: {customer_info_str}.
            """
        ),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}")

    ]

)

agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools = []
)

agent2 = create_tool_calling_agent(
    llm = llm,
    prompt = prompt2,
    tools = []
)


agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
agent_executor2 = AgentExecutor(agent=agent2, tools=[], verbose=True)


# -----------------Streamlit execution---------------------------


# --- Initialize session states ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "application_started" not in st.session_state:
    st.session_state.application_started = False
if "img_after_login" not in st.session_state:
    st.session_state.img_after_login = None
if "view_investments" not in st.session_state:
    st.session_state.view_investments = False
if "view_tracker" not in st.session_state:
    st.session_state.view_tracker = True
if "monthly_nudge" not in st.session_state:
    st.session_state.monthly_nudge = False



if not st.session_state.logged_in:
    login()

# --- After login display type (1): Non-investors Homepage ---
elif not st.session_state.application_started and st.session_state.username in non_investors["Username"].values:
    bg_img = get_encoded_bg("BPIhome_noninvestor.png")
    if apply_BPIapp_background_css(bg_img):
        st.session_state.application_started = True

# --- After login display type (2): Non-investors Application Form ---
elif st.session_state.application_started and st.session_state.username in non_investors["Username"].values:
    username = st.session_state.username 
    customer_info_str = find_customer(username)
    bg_img = get_encoded_bg("Application_bg.png")

    # --- Display floating button using Streamlit ---
    with st.container():
        chatbot_button_css()
        if st.button("💬", key="chat_toggle"):
            toggle_chat()

    apply_background_with_chatbtn_css(bg_img, blur=st.session_state.show_chat)

    # --- Chat box ---
    if st.session_state.show_chat:

        if "messages" not in st.session_state:         #initializing chat history
            st.session_state.messages = [
                {"role":"assistant", 
                "content": f"Hi, {username}! I'm Investie! Ask me anything about BPI investments!"""}
            ]

        for msg in st.session_state.messages:  #display past messages
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])


        if query := st.chat_input("Type your question here..."):    #chat input box
            st.session_state.messages.append({"role":"user", "content":query}) #add user message to history
            with st.chat_message("user"):
                st.markdown(query)
            
            raw_response = agent_executor.invoke({"query": query, "customer_info_str": customer_info_str})
            parsed_response = parser.parse(raw_response["output"])

            structured_response = (         # the actual output on GUI
                f"**Topic:** {parsed_response.topic}\n\n"
                f"**Summary:** {parsed_response.summary}\n\n"
                f"**Sources:** {', '.join(parsed_response.sources)}\n\n"
                #f"**Tools Used:** {', '.join(parsed_response.tools_used)}"
            )

            st.session_state.messages.append({"role":"assistant", "content": structured_response})
            with st.chat_message("assistant"):
                st.markdown(structured_response)

        st.markdown("</div>", unsafe_allow_html=True)



# --- After login display type (3): Investors Homepage --- 
elif st.session_state.username not in non_investors["Username"].values:
    username = st.session_state.username
    customer_info_str = find_customer(username)
    user_data = df[df['Username'] == username].iloc[0] 
    bg_img = get_encoded_bg("investment_page.png")


    if st.session_state.view_tracker:
        display_tracker(user_data)


    if username == "ana456" and not st.session_state.monthly_nudge:
        monthly_nudge_msg = agent_executor2.invoke({
            "input": "Generate this month's nudge", 
            "customer_info_str": customer_info_str
            })
        st.toast(monthly_nudge_msg["output"])
        st.session_state.monthly_nudge = True


    

    if not st.session_state.view_investments:
        if st.button("My Investments", key="investment_view"):
            st.session_state.view_investments = True
            st.session_state.view_tracker = False
            
        

    elif not st.session_state.view_tracker:
        
            
        # --- Display floating button using Streamlit ---
        with st.container():
            chatbot_button_css()
            if st.button("💬", key="chat_toggle"):
                toggle_chat()

        apply_background_with_chatbtn_css(bg_img, blur=st.session_state.show_chat)

        # --- Chat box ---
        if st.session_state.show_chat:

            if "messages" not in st.session_state:         #initializing chat history
                st.session_state.messages = [
                    {"role":"assistant", 
                    "content": f"Hi, {username}! I'm Investie! Ask me anything about BPI investments!"""}
                ]

            for msg in st.session_state.messages:  #display past messages
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])


            if query := st.chat_input("Type your question here..."):    #chat input box
                st.session_state.messages.append({"role":"user", "content":query}) #add user message to history
                with st.chat_message("user"):
                    st.markdown(query)

                customer_info_str = find_customer(username)
                raw_response = agent_executor.invoke({"query": query, "customer_info_str": customer_info_str})
                parsed_response = parser.parse(raw_response["output"])

                structured_response = (         # the actual output on GUI
                    f"**Topic:** {parsed_response.topic}\n\n"
                    f"**Summary:** {parsed_response.summary}\n\n"
                    f"**Sources:** {', '.join(parsed_response.sources)}\n\n"
                    #f"**Tools Used:** {', '.join(parsed_response.tools_used)}"
                )

                st.session_state.messages.append({"role":"assistant", "content": structured_response})
                with st.chat_message("assistant"):
                    st.markdown(structured_response)

            st.markdown("</div>", unsafe_allow_html=True)



    

