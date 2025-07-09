# app.py

import streamlit as st
from utils import save_score, show_leaderboard

# Global score
if "global_score" not in st.session_state:
    st.session_state.global_score = 0

# Player name
st.sidebar.title("🎮 Player Info")

# Initialize state if not set
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# Get name only if not already set
if st.session_state.player_name == "":
    name_input = st.sidebar.text_input("Enter your name:", key="name_input")
    if name_input:
        st.session_state.player_name = name_input
        st.rerun()
else:
    st.sidebar.markdown(f"👋 Hello, **{st.session_state.player_name}**")

# Track if user exited
if "exit_game" not in st.session_state:
    st.session_state.exit_game = False

# Title and game selector
st.title("🧠 Brain Fitness Game")
st.markdown(f"### 🌟 Global Score: `{st.session_state.global_score}`")

game = st.selectbox("Choose a game", ["Memory Match", "Quick Math", "Number Recall"], key="game_selector")
if st.session_state.exit_game:
    st.success("👋 Thanks for playing! You may now close this tab.")
    st.stop()

# Load selected game
if game == "Memory Match":
    from memory_match import run_memory_match
    run_memory_match()
elif game == "Quick Math":
    from quick_math import run_quick_math
    run_quick_math()
elif game == "Number Recall":
    from number_recall import run_number_recall
    run_number_recall()

# Show leaderboard
st.markdown("---")
show_leaderboard(st)

if st.button("🚪 Exit Game"):
    st.session_state.exit_game = True
    st.rerun()
