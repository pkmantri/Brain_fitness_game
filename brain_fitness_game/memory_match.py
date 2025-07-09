# memory_match.py

import streamlit as st
import random
from PIL import Image
import os
import time
import base64
from utils import save_score

def run_memory_match():
    st.subheader("🧩 Memory Match Game")

    card_folder = os.path.join(os.path.dirname(__file__), "assets/cards")
    card_names = [
        "apple.png", "basketball.png", "dog.png",
        "heart.png", "stack-of-books.png", "strawberry-cake.png"
    ]

    if "cards" not in st.session_state:
        cards = card_names * 2
        random.shuffle(cards)
        st.session_state.cards = cards
    else:
        cards = st.session_state.cards

    if "flipped" not in st.session_state:
        st.session_state.flipped = []
        st.session_state.matched = []
        st.session_state.score = 0
        st.session_state.moves = 0
        st.session_state.start_time = time.time()

    def play_sound():
        sound_file = os.path.join(os.path.dirname(__file__), "assets/match.wav")
        if os.path.exists(sound_file):
            with open(sound_file, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            b64 = base64.b64encode(audio_bytes).decode()
            md = f"""
                <audio autoplay>
                    <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
            """
            st.markdown(md, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, card in enumerate(cards):
        with cols[i % 4]:
            if i in st.session_state.matched or i in st.session_state.flipped:
                img = Image.open(os.path.join(card_folder, card))
                st.image(img, use_container_width=True)
            else:
                if st.button("❓", key=f"card_{i}"):
                    if len(st.session_state.flipped) < 2 and i not in st.session_state.flipped:
                        st.session_state.flipped.append(i)
                        st.rerun()

    if len(st.session_state.flipped) == 2:
        first, second = st.session_state.flipped
        if cards[first] == cards[second]:
            st.session_state.matched.extend([first, second])
            st.session_state.score += 10
            st.session_state.global_score += 10
            play_sound()
        st.session_state.moves += 1
        time.sleep(1)
        st.session_state.flipped = []
        st.rerun()

    st.markdown("---")
    st.markdown(f"**🏆 Score:** {st.session_state.score} | **🧮 Moves:** {st.session_state.moves}")

    if len(st.session_state.matched) == len(cards):
        total_time = int(time.time() - st.session_state.start_time)
        st.balloons()
        st.success(f"🎉 Completed in {st.session_state.moves} moves and {total_time}s")

        save_score(st.session_state.player_name, st.session_state.global_score)

        if st.button("🔁 Restart Game"):
            for key in ["cards", "flipped", "matched", "score", "moves", "start_time"]:
                st.session_state.pop(key, None)
            st.rerun()
