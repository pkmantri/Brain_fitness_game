# number_recall.py

import streamlit as st
import random
import time
from utils import save_score

def run_number_recall():
    st.subheader("🔢 Number Recall Game")

    if "nr_stage" not in st.session_state:
        st.session_state.nr_stage = "show"
        st.session_state.nr_score = 0
        st.session_state.nr_round = 1
        st.session_state.nr_number = ""
        st.session_state.nr_start_time = time.time()
        st.session_state.nr_score_history = []

    def generate_number(length):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    if st.session_state.nr_stage == "show":
        length = 3 + st.session_state.nr_round - 1
        st.session_state.nr_number = generate_number(length)
        st.markdown(f"### Memorize: `{st.session_state.nr_number}`")
        time.sleep(3)
        st.session_state.nr_stage = "recall"
        st.rerun()

    elif st.session_state.nr_stage == "recall":
        answer = st.text_input("Enter the number")

        if st.button("Submit", key="submit_nr"):
            if answer == st.session_state.nr_number:
                st.success("✅ Correct!")
                st.session_state.nr_score += 10
                st.session_state.global_score += 10
            else:
                st.error(f"❌ Correct: {st.session_state.nr_number}")
            st.session_state.nr_score_history.append(st.session_state.nr_score)
            st.session_state.nr_round += 1
            st.session_state.nr_stage = "show"
            st.rerun()

    st.markdown("---")
    st.markdown(f"**🏆 Score:** {st.session_state.nr_score} | **🔁 Round:** {st.session_state.nr_round - 1}")
    st.line_chart(st.session_state.nr_score_history)

    if st.session_state.nr_round > 10:
        total_time = int(time.time() - st.session_state.nr_start_time)
        st.success(f"🎉 Finished in {total_time}s")

        save_score(st.session_state.player_name, st.session_state.global_score)

        if st.button("🔁 Play Again"):
            for key in ["nr_score", "nr_round", "nr_stage", "nr_number", "nr_start_time", "nr_score_history"]:
                st.session_state.pop(key, None)
            st.rerun()
