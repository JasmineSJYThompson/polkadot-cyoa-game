import streamlit as st
import json
import os

BASE_DIR = os.getcwd()+"/iteration0/"

# Load scenes
with open(BASE_DIR+"json_files/scenes.json", "r") as f:
    scenes = json.load(f)["scenes"]

# State initialization
if "current" not in st.session_state:
    st.session_state.current = "start_city_edge"
if "history" not in st.session_state:
    st.session_state.history = []
if "decision_text" not in st.session_state:
    st.session_state.decision_text = None
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "scene"  # Default page mode is scene page mode

# Developer Mode (enabled always)
DEVELOPER_MODE = True

# Custom CSS for styling the game
st.markdown("""
<style>
body {
    background-color: #000000;
    color: #00FFCC;
    font-family: 'Courier New', monospace;
}
h1, h2, h3 {
    color: #00FFCC;
}
button {
    color: #000000 !important;
    background-color: #00FFCC !important;
    border-radius: 4px !important;
}
code {
    color: #00FFCC !important;
}
</style>
""", unsafe_allow_html=True)

def get_scene_description(scene_name):
    """Retrieve scene description from a file."""
    scene_file = f"scenes/{scene_name}.txt"
    if os.path.exists(scene_file):
        with open(BASE_DIR+scene_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Scene description not found."

def get_decision_text(decision_name):
    """Retrieve decision text from a file."""
    decision_file = f"decisions/{decision_name}.txt"
    if os.path.exists(decision_file):
        with open(BASE_DIR+decision_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Decision text not found."

def get_ascii_art(scene_name):
    """Retrieve ASCII art for a scene."""
    path = f"ascii_art/{scene_name}.asc"
    if os.path.exists(path):
        with open(BASE_DIR+path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Show current scene info
current = st.session_state.current
scene = scenes[current]

# Scene Page Mode
if st.session_state.page_mode == "scene":
    st.markdown(f"### Scene: `{current}`")

    # Show the scene description
    st.markdown("---")
    st.markdown(get_scene_description(current))

    # Show decision options if choices exist
    if "choices" in scene:
        st.markdown("---")
        st.markdown("### What do you do?")
        options = list(scene["choices"].keys())
        for i, choice in enumerate(options, 1):
            label = choice.replace("_", " ").capitalize()
            if st.button(f"{i}. {label}", key=f"choice_{i}"):
                # Save history and transition to the new scene
                st.session_state.history.append(current)
                st.session_state.current = scene["choices"][choice]
                
                # Store the decision text
                st.session_state.decision_text = get_decision_text(choice)
                st.session_state.page_mode = "bridging_text"  # Move to bridging text page
                st.rerun()

        # "Back" and "Restart" buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Back") and st.session_state.history:
                st.session_state.current = st.session_state.history.pop()
                st.session_state.page_mode = "scene"  # Go back to scene page
                st.rerun()
        with col2:
            if st.button("Restart"):
                st.session_state.current = "start_city_edge"
                st.session_state.history.clear()
                st.session_state.page_mode = "scene"  # Reset to scene
                st.rerun()

    # If the scene has no choices, move to end or continue
    else:
        st.markdown("---")
        st.success("→ End of path.")
        if st.button("Continue"):
            st.session_state.page_mode = "bridging_text"
            st.rerun()

# Bridging Text Page Mode (display the decision text with "Continue" button)
elif st.session_state.page_mode == "bridging_text":
    # Retrieve the decision text that led to this scene
    decision_made = None
    for choice, next_scene in scene["choices"].items():
        if next_scene == st.session_state.current:
            decision_made = choice
            break

    # If a decision was found, display its text
    if decision_made:
        st.markdown(f"### Decision: `{decision_made.replace('_', ' ').capitalize()}`")
        decision_text = st.session_state.decision_text  # Use stored decision text
        st.markdown(f"**→ {decision_text}**")  # Display decision text
    
    # Show ASCII Art (if available)
    ascii_art = get_ascii_art(current)
    if ascii_art:
        st.code(ascii_art, language="")

    # Display Continue Button to proceed
    if st.button("Continue"):
        # Update the current scene based on the user's choice
        st.session_state.history.append(current)
        st.session_state.page_mode = "scene"  # Move back to the scene page
        st.rerun()
