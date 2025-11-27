import streamlit as st
from dotenv import load_dotenv
import os

# ⚡ Load environment variables early
load_dotenv()

print("GROQ_API_KEY loaded:", os.environ.get("GROQ_API_KEY"))  # Debug check

from agents.groq_llm import GroqLLM
from agents.plan_creator import generate_learning_plan
from agents.plan_executor import execute_learning_plan
from agents.quiz_agent import generate_quiz
from agents.feedback_agent import get_feedback

# Initialize session state
for key, default in [
    ("topic", ""),
    ("level", "Beginner"),
    ("time_hours", 10),
    ("plan", []),
    ("explanation", ""),
    ("quiz_data", []),
    ("quiz_started", False),
    ("score", 0),
    ("feedback", "")
]:
    if key not in st.session_state:
        st.session_state[key] = default

st.title("AI E-Learning App")

topic_input = st.text_input("Enter your learning topic/goal:", st.session_state.topic)
level = st.selectbox(
    "Select your learning level:",
    ["Beginner", "Intermediate", "Advanced"],
    index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.level)
)
time_hours = st.number_input(
    "Enter number of hours to spend learning:",
    min_value=1,
    max_value=100,
    value=st.session_state.time_hours
)

if st.button("Create Plan"):
    if topic_input.strip() == "":
        st.error("Please enter a valid topic!")
    else:
        st.session_state.topic = topic_input.strip()
        st.session_state.level = level
        st.session_state.time_hours = time_hours
        st.session_state.plan = generate_learning_plan(
            st.session_state.topic,
            st.session_state.level,
            st.session_state.time_hours
        )
        st.session_state.explanation = ""
        st.session_state.quiz_data = []
        st.session_state.quiz_started = False
        st.success("Plan created!")

if st.session_state.plan:
    st.markdown("### Generated Learning Plan:")
    if isinstance(st.session_state.plan, list):
        for i, step in enumerate(st.session_state.plan, 1):
            st.write(f"{i}. {step}")
    else:
        st.write(st.session_state.plan)

if st.session_state.plan and st.button("Execute Plan"):
    st.session_state.explanation = execute_learning_plan(st.session_state.plan)
    st.session_state.quiz_data = []
    st.session_state.quiz_started = False
    st.success("Plan executed and explained!")

if st.session_state.explanation:
    st.markdown("### Explanation of the Plan")
    st.write(st.session_state.explanation)

if st.session_state.explanation and not st.session_state.quiz_started:
    if st.button("Start Quiz"):
        st.session_state.quiz_data = generate_quiz(st.session_state.topic, num_questions=20)
        st.session_state.quiz_started = True
        st.session_state.score = 0

if st.session_state.quiz_started and st.session_state.quiz_data:
    st.markdown("## Quiz Time!")
    with st.form(key="quiz_form"):
        for i, q in enumerate(st.session_state.quiz_data):
            st.write(f"Q{i+1}. {q['question']}")
            user_answer = st.radio("Select your answer:", q["options"], key=f"q{i}")
            st.session_state[f"user_answer_{i}"] = user_answer

        submit = st.form_submit_button("Submit Quiz")
        if submit:
            score = 0
            for i, q in enumerate(st.session_state.quiz_data):
                if st.session_state.get(f"user_answer_{i}", "") == q["answer"]:
                    score += 1
            st.session_state.score = score
            st.success(f"Your score: {score} / {len(st.session_state.quiz_data)}")
            st.session_state.quiz_started = False
            st.session_state.quiz_data = []


