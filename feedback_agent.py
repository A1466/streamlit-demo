from agents.groq_llm import GroqLLM

llm = GroqLLM()

def get_feedback(score, total, topic):
    prompt = f"""
You are an intelligent education feedback assistant helping a student improve in their learning journey.

Topic: {topic}
Quiz Score: {score} out of {total}

Based on this, provide a personalized and constructive feedback covering the following points:

1. **Performance Analysis**: 
   - Evaluate the student's performance level (excellent, good, average, needs improvement).
   - Comment on their accuracy percentage and what it reflects about their understanding of the topic.

2. **Strengths Identified**: 
   - Based on the score, what concepts or areas might the learner already be strong in?
   - Mention any general confidence the learner might have built in the topic.

3. **Weak Areas & Recommendations**: 
   - Suggest areas or subtopics within "{topic}" the student might need to review or revisit.
   - Offer tips for improving performance (e.g., reading strategies, practice quizzes, concept reinforcement).

4. **Study Plan Adjustment (Optional)**:
   - If the score is below average, suggest changes to the learning plan or time allocation.
   - Recommend resources like videos, blogs, or specific exercises that might help.

5. **Motivational Statement**:
   - End with a short, motivating message encouraging the learner to keep going and improve.

Output the feedback in clear paragraphs or bullet points.
Avoid repeating the prompt. Keep it friendly, helpful, and positive in tone.
"""
    return llm._call(prompt)
