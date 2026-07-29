from turtle import onclick

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import json
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os


from langchain_groq import ChatGroq

if "voice_started" not in st.session_state:
    st.session_state.voice_started = False

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "conversation" not in st.session_state:
    st.session_state.conversation = ""

if "feedback_report" not in st.session_state:
    st.session_state.feedback_report = ""

# Load model once
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="Your key"
    
st.set_page_config(page_title="Interview Agent", layout="wide")

# read q file
with open('question.json', 'r') as file:
    question_bank = json.load(file)

# st.title("Interview Agent")
    
menu=st.sidebar.radio(
  "Navigation",
  [
    "Home",
    "Profile",
    "Assessments",
    "Mock Interviews",
    "Interview Questions",
    "Progress Tracker"
  ]
)

if 'scores' not in st.session_state:
    st.session_state.scores = []
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'role' not in st.session_state:
    st.session_state.role = ""
    
#---------Home Page----------------
if menu=="Home":
    st.title(":blue[AI Interview Preparation System!]")
    st.markdown("""
    ### Crack your interviews with our AI-powered Interview Preparation System! Our platform offers a comprehensive suite of tools to help you prepare for your interviews effectively. 
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Student Practicing", ":blue[100+]")
    col2.metric("Questions Available", ":blue[500+]")
    col3.metric("Success Rate", ":blue[87%]")
    
    st.divider()
    
    st.subheader("How It Works")
    col1, col2= st.columns(2)
    
    with col1:
      st.info("Skill Assessment")
      st.info("weak Topic Detection")
      
    with col2:
      st.info("Interview Questions")
      st.info("Progress Tracking")
      
    st.divider()
    st.success("Get started by navigating through the sidebar to explore the features of the Interview Agent. You can take mock interviews, assess your skills, and track your progress over time.")
    
elif menu=="Profile":
    st.title(":blue[Profile]")
    name = st.text_input("Enter your name",key="name")
    
    role=st.selectbox("Select your role",["Select Role","Data Analyst","Data Scientist","Machine Learning Engineer","Software Engineer","Business Analyst","Product Manager","Full Stack Developer","Backend Developer","Frontend Developer","UI/UX  Designer"],key="role")
    
    Degree=st.selectbox("Select your Degree",["Select Degree","Btech","Mtech","BCA","MCA","BSc","MSc","MBA"],key="degree")
    
    year=st.selectbox("Select your Year",["Select Year","1st Year","2nd Year","3rd Year","4th Year"],key="year")
    
    if st.button(":green[Save Profile]"):

     if name == "" or Degree == "Select Degree" or role == "Select Role" or year == "Select Year":
        st.error("Kindly fill all the details.")

     else:
        st.session_state.student_name = name
        st.session_state.student_role = role

        st.success(
            f"Profile saved for {st.session_state.student_name} as {st.session_state.student_role}."
        )

elif menu=="Assessments":
    st.title(":blue[Assessments]")
    st.markdown("Rate yourself out of 100")
    arrays = st.slider("Arrays", 0, 100, 50)
    strings = st.slider("Strings", 0, 100, 50)
    linked_lists = st.slider("Linked Lists", 0, 100, 50)
    oops = st.slider("OOPS", 0, 100, 50)
    dbms = st.slider("DBMS", 0, 100, 50)
    
    if st.button(":red[Analyze Skills]"):
        
        st.session_state.scores ={
           "Arrays": arrays,
           "Strings": strings,  
          "Linked Lists": linked_lists,
          "OOPS": oops,
           "DBMS": dbms
        }
        st.success(":green[Skills analyzed successfully!]")
        

elif menu =="Interview Questions":
    
    st.title(":blue[Interview Preparation Questions]")

    topic = st.selectbox(
        "Select Topic",
        ["Introduction", "Arrays", "OOPS", "SQL", "AI/ML", "UIUX"]
    )

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button(":green[Generate Question]"):

        prompt = f"""
        Generate 5 {difficulty} level interview questions
        on the topic {topic}.

Return each question on a new line.
"""

        response = llm.invoke(prompt)

        st.success(response.content)
    
    
    
elif menu == "Mock Interviews":

    st.title("🎤 AI Voice Mock Interview")

    role = st.selectbox(
        "Select Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Software Engineer",
            "Machine Learning Engineer"
        ]
    )

    if st.button("Start Interview"):

        first_question = llm.invoke(
            f"""
            You are an interviewer.

            Start a mock interview for a {role}.

            Ask only one interview question.
            """
        )

        st.session_state.current_question = first_question.content
        st.session_state.voice_started = True
        st.session_state.question_count = 1
        st.session_state.conversation = ""

    if st.session_state.voice_started:

        st.subheader(
            f"Question {st.session_state.question_count}"
        )

        st.info(st.session_state.current_question)

        # AI Voice
        tts = gTTS(st.session_state.current_question)

        tts.save("question.mp3")

        st.audio("question.mp3")

        st.markdown("### 🎤 Speak Your Answer")

        answer = speech_to_text(
            language="en",
            start_prompt="Start Recording",
            stop_prompt="Stop Recording",
            key=f"speech_{st.session_state.question_count}"
        )

        if answer:

            st.success("Answer Recorded")

            st.write(answer)

            st.session_state.conversation += f"""
            Question:
            {st.session_state.current_question}

            Answer:
            {answer}
            """

            if st.session_state.question_count < 5:

                next_question = llm.invoke(
                    f"""
                    You are conducting a mock interview.

                    Candidate Role:
                    {role}

                    Previous Question:
                    {st.session_state.current_question}

                    Candidate Answer:
                    {answer}

                    Ask one relevant follow-up question.
                    """
                )

                st.session_state.current_question = (
                    next_question.content
                )

                st.session_state.question_count += 1

                st.rerun()

            else:

                report = llm.invoke(
                    f"""
                    Analyze this interview:

                    {st.session_state.conversation}

                    Generate:

                    Overall Score /100

                    Technical Skills

                    Communication Skills

                    Confidence Level

                    Strengths

                    Weaknesses

                    Suggestions
                    """
                )

                st.session_state.feedback_report = (
                    report.content
                )

                st.session_state.voice_started = False

    if st.session_state.feedback_report:

        st.subheader("📊 Final Interview Report")

        st.write(
            st.session_state.feedback_report
        )
        
elif menu =="Progress Tracker":
    st.title(":blue[Progress Tracker]")
    st.markdown("Track your progress over time and identify areas for improvement.")
    
    if not st.session_state.scores:
        st.warning("No assessment scores available. Please take an assessment first.")
    else:
        scores=st.session_state.scores
        df=pd.DataFrame({"Topic":list(scores.keys()),"Score":list(scores.values())})
        scores_df = pd.DataFrame([st.session_state.scores])
        st.line_chart(scores_df.T, width=700, height=400)
        col1,col2,col3=st.columns(3)
        avg_score=sum(scores.values())/len(scores)
      
        weak_topics=[k for k , v in scores.items() if v<50]
        strong_topics=[k for k , v in scores.items() if v>70]
        col1.metric("Average Score", f"{avg_score: 2f}%")
        col2.metric("Weak Topic", len(weak_topics))
        col3.metric("Strong Topic", len(strong_topics))
        
        st.subheader("Topic Performance")
        fig, ax = plt.subplots(figsize=(5,2.5))
        ax.bar(df["Topic"],df["Score"])
        plt.xticks(rotation=20)
        st.pyplot(fig)
        
        if weak_topics:
          for topic in weak_topics:
            st.error(f"Weak Topic:{topic}")
        else:
          st.success("No weak Topic Detected")
          
        st.subheader("Strong_topics")
        if strong_topics:
         st.success(f"Strong Topics : {topic}")
          
    st.markdown("Visualize your performance and progress over time.")
        
