import streamlit as st
import json
import time
import os

st.set_page_config(page_title="🔮 Chrome Gilgamesh Terminal", layout="wide")
st.title("🔮 Chrome Gilgamesh Terminal")

# Load scenes
with open("json_files/scenes.json", "r") as f:
    scenes = json.load(f)["scenes"]

# Init state
if "current" not in st.session_state:
    st.session_state.current = "start_city_edge"
if "history" not in st.session_state:
    st.session_state.history = []
if "terminal_log" not in st.session_state:
    st.session_state.terminal_log = []

# Util functions
def typewriter(text, delay=0.02):
    placeholder = st.empty()
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(f"""
{typed}
""")
        time.sleep(delay)
    return typed

def get_scene_description(scene_name):
    path = f"scenes/{scene_name}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Scene description not found."

def get_decision_text(decision):
    path = f"decisions/{decision}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Decision text not found."

def get_ascii_art(scene_name):
    path = f"ascii_art/{scene_name}.asc"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Layout
left, right = st.columns([2, 1])

scene = scenes[st.session_state.current]
choices = scene["choices"].keys()

# Choice and input area
with right:
    if "choices" in scene:
        st.subheader("💬 What do you do?")
        for i, choice in enumerate(choices, 1):
            label = choice.replace("_", " ").capitalize()
            if st.button(f"{i}. {label}"):
                decision_text = get_decision_text(choice)
                typed_decision = typewriter(decision_text)
                st.session_state.terminal_log.append(typed_decision)
                st.session_state.history.append(st.session_state.current)
                st.session_state.current = scene["choices"][choice]

        st.markdown("---")
        if st.button("🔁 Restart"):
            st.session_state.current = "start_city_edge"
            st.session_state.history.clear()
            st.session_state.terminal_log.clear()
            st.rerun()

        if st.button("🔙 Back") and st.session_state.history:
            st.session_state.current = st.session_state.history.pop()
            st.rerun()
    else:
        st.success("→ End of path. Click to restart.")
        if st.button("Start Over"):
            st.session_state.current = "start_city_edge"
            st.session_state.history.clear()
            st.session_state.terminal_log.clear()
            st.rerun()

# Terminal output area
with left:
    st.subheader(f"📍 Scene: `{st.session_state.current}`")

    # Scene description
    scene_text = get_scene_description(st.session_state.current)
    output = typewriter(scene_text)
    st.session_state.terminal_log.append(output)

    # ASCII art
    art = get_ascii_art(st.session_state.current)
    if art:
        st.code(art)
    
    st.rerun()