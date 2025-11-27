from agents.groq_llm import GroqLLM
import re

llm = GroqLLM()

def generate_quiz(topic_text, num_questions=20):
    prompt = (
        f"Create a quiz with {num_questions} multiple choice questions based on the topic: '{topic_text}'.\n"
        f"For each question, provide 4 options labeled a), b), c), d) and indicate the correct answer.\n"
        f"Format the output like this:\n"
        f"Question 1: ...\n"
        f"a) option1\n"
        f"b) option2\n"
        f"c) option3\n"
        f"d) option4\n"
        f"Answer: a\n\n"
        f"Generate all {num_questions} questions in this format."
    )
    
    raw_output = llm._call(prompt)

    quiz = []
    questions_raw = re.split(r'Question\s*\d+:', raw_output, flags=re.IGNORECASE)
    
    for q_text in questions_raw[1:]:
        lines = [line.strip() for line in q_text.strip().split('\n') if line.strip()]
        if not lines:
            continue
        question = lines[0]
        options = []
        answer = None

        for line in lines[1:]:
            if re.match(r'^[abcd]\)', line, re.IGNORECASE):
                options.append(line[2:].strip())
            elif line.lower().startswith("answer:"):
                ans_letter = line.split(":", 1)[1].strip().lower()
                if ans_letter in ['a','b','c','d'] and len(options) >= 4:
                    answer = options[ord(ans_letter) - ord('a')]

        if question and len(options) == 4 and answer:
            quiz.append({
                "question": question,
                "options": options,
                "answer": answer
            })
        if len(quiz) >= num_questions:
            break

    return quiz
