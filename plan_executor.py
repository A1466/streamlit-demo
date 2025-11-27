from agents.groq_llm import GroqLLM
import streamlit as st

llm = GroqLLM()

def execute_learning_plan(plan_text, step_number=None):
    if step_number:
        prompt = (
            f"You are an expert tutor. Provide a thorough, in-depth explanation of step number {step_number} "
            f"from this learning plan:\n{plan_text}\n\n"
            "Your explanation should cover every detail of this step from start to finish. Include:\n"
            "- Clear conceptual explanations,\n"
            "- Real-world examples,\n"
            "- Sample code snippets or practical demonstrations if applicable,\n"
            "- Step-by-step guidance,\n"
            "- Common pitfalls or misconceptions to avoid,\n"
            "- Tips for practicing or reinforcing the concept,\n"
            "- Any relevant analogies or visualizations to aid understanding.\n\n"
            "Make the explanation beginner-friendly but comprehensive enough for intermediate learners too."
        )
    else:
        
        prompt = (
            f"You are an expert tutor. Provide a thorough, in-depth explanation of the entire learning plan:\n{plan_text}\n\n"
            "Explain each step carefully and include:\n"
            "- Conceptual details,\n"
            "- Examples and code snippets where appropriate,\n"
            "- Stepwise instructions,\n"
            "- Common mistakes to avoid,\n"
            "- Tips to reinforce learning.\n\n"
            "Make the explanation clear, detailed, and engaging."
        )

    response = llm._call(prompt)

    
    st.session_state.current_topic = plan_text if not step_number else f"Step {step_number} from: {plan_text}"

    return response

