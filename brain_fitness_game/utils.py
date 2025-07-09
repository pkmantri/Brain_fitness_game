# utils.py
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def save_score(player, score):
    if not player:
        return

    # Load existing data safely
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    # Add and sort top scores
    data.append({"name": player, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:5]

    # Save updated data
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_leaderboard(st):
    st.markdown("## 🏅 Leaderboard (Top 5)")
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            st.warning("⚠️ Leaderboard data corrupted. Resetting...")
            data = []
            with open(LEADERBOARD_FILE, "w") as f:
                json.dump([], f)

        if not data:
            st.info("No scores yet.")
        else:
            for idx, entry in enumerate(data, 1):
                st.markdown(f"**{idx}. {entry['name']}** — {entry['score']} points")
    else:
        st.info("No scores yet.")
