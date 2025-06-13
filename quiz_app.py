
import streamlit as st
import json
import os
import random

# Set the folder containing chapter JSON files
QUIZ_FOLDER = "HRQuizFiles"

# Load questions from selected chapters
@st.cache_data
def load_questions(selected_chapters):
    questions = []
    for ch in selected_chapters:
        file_path = os.path.join(QUIZ_FOLDER, f"HR_Chapter{ch}_ALL_Questions.json")
        try:
            with open(file_path, "r") as f:
                questions += json.load(f)
        except Exception as e:
            st.error(f"Could not load Chapter {ch}: {e}")
    random.shuffle(questions)
    return questions

# UI
st.title("Human Resources Quiz App")

# Chapter selection
chapter_options = [str(i) for i in range(1, 8)]
selected = st.multiselect("Select Chapters to Include", chapter_options, default=chapter_options)

# Initialize session state
if selected and "questions" not in st.session_state:
    st.session_state.questions = load_questions(selected)
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.total = len(st.session_state.questions)
    st.session_state.feedback = ""
    st.session_state.show_next = False
    st.session_state.quiz_over = False

# Quiz logic
if selected and not st.session_state.quiz_over:
    q = st.session_state.questions[st.session_state.q_index]
    st.subheader(f"Question {st.session_state.q_index + 1} of {st.session_state.total}")
    st.write(q["question"])
    choice = st.radio("Select an answer:", q["choices"], key=st.session_state.q_index)

    if not st.session_state.show_next and st.button("Submit Answer"):
        correct_answer = q["choices"][ord(q["answer"]) - ord("A")]
        if choice == correct_answer:
            st.session_state.feedback = "✅ Correct!"
            st.session_state.score += 1
        else:
            st.session_state.feedback = f"❌ Incorrect. Correct answer: {correct_answer}"
        st.session_state.show_next = True

    if st.session_state.show_next:
        st.info(st.session_state.feedback)
        if st.button("Next Question"):
            st.session_state.q_index += 1
            st.session_state.show_next = False
            st.session_state.feedback = ""
            if st.session_state.q_index >= st.session_state.total:
                st.session_state.quiz_over = True
            st.rerun()

elif selected and st.session_state.quiz_over:
    st.subheader("🎉 Quiz Complete!")
    st.write(f"Final Score: **{st.session_state.score} / {st.session_state.total}**")
    if st.button("Restart Quiz"):
        for key in ["questions", "q_index", "score", "total", "feedback", "show_next", "quiz_over"]:
            st.session_state.pop(key, None)
        st.rerun()
