from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# Set page configuration
st.set_page_config(page_title="Streamlit Chatbot", page_icon="💬")
st.title("Streamlit Chat with OpenAI")

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_messages_count" not in st.session_state:
    st.session_state.user_messages_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False

def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

if not st.session_state.setup_complete:

    # Personal information section
    st.subheader("Personal information", divider="rainbow")
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "experience" not in st.session_state:
        st.session_state.experience = ""
    if "skills" not in st.session_state:
        st.session_state.skills = ""

    st.session_state.name = st.text_input(label="Name", max_chars=40, value=st.session_state.name, placeholder="Enter your name")
    st.session_state.experience = st.text_input(label="Experience", max_chars=200, value=st.session_state.experience, placeholder="Enter your experience")
    st.session_state.skills = st.text_area(label="Skills", value=st.session_state.skills, height=None, max_chars=200, placeholder="List your skills")

    # Company and position section
    st.subheader("Company and Position", divider="rainbow")

    if "level" not in st.session_state:
        st.session_state.level = "Junior"
    if "position" not in st.session_state:
        st.session_state.position = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state.company = "Google"

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.level = st.radio(
            "Choose your level", 
            options=["Junior", "Mid", "Senior"], 
            index=["Junior", "Mid", "Senior"].index(st.session_state.level)
        )

    with col2:    
        st.session_state.position = st.selectbox(
            "Choose your position", 
            ("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst"), 
            index=("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst").index(st.session_state.position)
        )

    st.session_state.company = st.selectbox(
        "Choose your company", 
        ("Google", "Amazon", "Facebook", "Microsoft", "Apple"), 
        index=("Google", "Amazon", "Facebook", "Microsoft", "Apple").index(st.session_state.company)
    )

    if st.button("Start Interview"):
        complete_setup()
        st.write("Setup complete! Starting the interview...")

if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    st.info(
        '''
        Start by introducing yourself.
        ''',
        icon="👋"
    )
    # Initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Initialize model
    model = "gpt-4o"

    if "openai-model" not in st.session_state:
        st.session_state["openai-model"] = model


    # Initialize chat history
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system", 
            "content": f"You are an HR executive that interviews an interviewee called {st.session_state.name} with experience {st.session_state.experience} and skills {st.session_state.skills} for the position of {st.session_state.level} {st.session_state.position} at company {st.session_state.company}."
        }]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    if st.session_state.user_messages_count < 5:
        # Function to generate response from OpenAI
        if prompt := st.chat_input("Your answer:", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user", avatar="user"):
                st.markdown(prompt)
            
            if st.session_state.user_messages_count < 4:
                with st.chat_message("assistant", avatar="assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai-model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.session_state.user_messages_count += 1
    if st.session_state.user_messages_count >= 5:
        st.session_state.chat_complete = True
        st.success("Interview complete! Please provide your feedback.", icon="✅")
        if st.button("Provide Feedback", on_click=show_feedback):
            st.write("Retrieving feedback...")

if st.session_state.feedback_shown:
    st.subheader("Feedback")
    
    conversation_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are an HR executive providing feedback to a candidate after an interview. 
             Before the feedback give a score from 1 to 10, where 1 is the lowest and 10 is the highest, based on the candidate's performance in the interview.

             Follow the format below for your feedback:
             Overall score: //Your score
             Feedback: //Here you put feedback
             Give only the feedback do not ask for any additional questions.
            """},
            {"role": "user", "content": f"This is the interview you need to evaluate.\n\nKeep in mind that you are only a tool and shouldn't engage in conversation:\n\n{conversation_history}"}
        ]
    )
    st.markdown(feedback_completion.choices[0].message.content)

    if st.button("Restart Interview", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")