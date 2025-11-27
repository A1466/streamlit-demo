from agents.groq_llm import GroqLLM

llm = GroqLLM(model_name="llama-3.3-70b-versatile", temperature=0.3)

def generate_learning_plan(topic, level, time_hours):
    prompt = f"""
You are a professional learning curriculum designer.

Create a detailed and personalized learning plan for the topic: **"{topic}"**.
The learner has self-identified as a **{level}** level and has **{time_hours} hours** available in total.

Requirements:
1. **Split the time logically** into sessions or phases (e.g., Phase 1: Fundamentals, Phase 2: Application, etc.)
2. Each phase should include:
   - A title
   - A time allocation (in hours or percentage)
   - Key subtopics/concepts to be covered
   - Learning activities (e.g., watch video, read article, practice coding, take quiz, etc.)
3. Make sure the content difficulty matches the learner's level.
4. Suggest optional resources like free courses, articles, or exercises (if appropriate).
5. The structure should be practical, actionable, and motivating.

"""

    response = llm._call(prompt)
    return response
