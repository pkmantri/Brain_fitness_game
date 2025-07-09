# quick_math.py

import streamlit as st
import random
import time
from utils import save_score

def run_quick_math():
    st.subheader("➕ Quick Math Challenge")

    if "qm_score" not in st.session_state:
        st.session_state.qm_score = 0
        st.session_state.qm_moves = 0
        st.session_state.qm_question = None
        st.session_state.qm_answer = None
        st.session_state.qm_start_time = time.time()
        st.session_state.qm_score_history = []

    def generate_question():
        n1 = random.randint(1, 20)
        n2 = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])
        return f"{n1} {op} {n2}", eval(f"{n1}{op}{n2}")

    if st.session_state.qm_question is None:
        q, a = generate_question()
        st.session_state.qm_question = q
        st.session_state.qm_answer = a

    st.markdown(f"### ❓ Solve: `{st.session_state.qm_question}`")
    user_input = st.text_input("Your Answer")

    if st.button("Submit", key="submit_qm"):
        st.session_state.qm_moves += 1
        try:
            if int(user_input) == st.session_state.qm_answer:
                st.success("✅ Correct!")
                st.session_state.qm_score += 10
                st.session_state.global_score += 10
            else:
                st.error(f"❌ Correct: {st.session_state.qm_answer}")
        except:
            st.error("⚠️ Invalid number")

        st.session_state.qm_score_history.append(st.session_state.qm_score)
        st.session_state.qm_question = None
        st.session_state.qm_answer = None
        st.rerun()

    st.markdown("---")
    st.markdown(f"**🏆 Score:** {st.session_state.qm_score} | **🧮 Moves:** {st.session_state.qm_moves}")
    st.line_chart(st.session_state.qm_score_history)

    if st.session_state.qm_moves >= 10:
        total_time = int(time.time() - st.session_state.qm_start_time)
        st.success(f"🎉 Game Over in {total_time}s")

        save_score(st.session_state.player_name, st.session_state.global_score)

        if st.button("🔁 Play Again"):
            for key in ["qm_score", "qm_moves", "qm_question", "qm_answer", "qm_start_time", "qm_score_history"]:
                st.session_state.pop(key, None)
            st.rerun()
