# InterviewPrep-Agent

🤖 AI Interview Preparation System

An intelligent Interview Preparation Platform built with Streamlit, LangChain, Groq LLM, and Speech Recognition that helps students practice technical interviews through AI-powered conversations.

The application simulates a real interviewer by asking role-specific interview questions, listening to spoken responses, generating follow-up questions, and finally providing detailed performance feedback.

🚀 Features
👤 Profile Management
Create and save candidate profile
Select job role, degree, and academic year
Personalised interview experience
📊 Skill Assessment

Users can self-evaluate their knowledge in topics such as:

Arrays
Strings
Linked Lists
OOPS
DBMS

The application stores assessment scores and later visualises them on the Progress Tracker.

💡 AI Interview Question Generator

Generate interview questions based on:

Topic
Difficulty Level
Job Role

Powered by Groq Llama 3.3 70B through LangChain.

Example topics include:

SQL
Arrays
OOPS
AI/ML
UI/UX
Introduction
🎤 AI Voice Mock Interview

The core feature of the application.

The interview process includes:

Candidate selects a target job role.
AI interviewer asks the first interview question.
Text-to-Speech converts the question into audio.
Candidate answers using voice.
Speech Recognition converts voice into text.
AI analyses the answer.
AI generates a relevant follow-up question.
The process continues for five interview rounds.

At the end of the interview, the complete conversation is analysed using an LLM.

📈 Interview Feedback Report

After completing the interview, the AI generates a comprehensive evaluation including:

Overall Interview Score
Technical Skills
Communication Skills
Confidence Level
Strengths
Weaknesses
Suggestions for Improvement

This provides candidates with actionable insights to improve future interviews.

📉 Progress Tracker

Visualises assessment performance using charts.

Features include:

Average Score
Weak Topics
Strong Topics
Performance Graph
Topic-wise Analysis

This helps candidates monitor their learning progress over time.

⚙️ Tech Stack
Frontend
Streamlit
Artificial Intelligence
LangChain
Groq API
Llama 3.3 70B Versatile
Speech Processing
Google Text-to-Speech (gTTS)
streamlit-mic-recorder
Data Handling
Pandas
JSON
Visualisation
Matplotlib
