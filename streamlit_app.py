import streamlit as st
# Must be the first Streamlit command
st.set_page_config(
    page_title="Choose Your Own Adventure",
    page_icon="🎮",
    layout="centered"
)

from blockchain_storage import BlockchainStorage
import logging
from typing import Dict
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cyoa_game.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def initialize_blockchain():
    """Initialize blockchain with seed phrase from secrets"""
    try:
        # Get seed phrase from Streamlit secrets
        seed_phrase = st.secrets["seed_phrase"]
        return BlockchainStorage(seed_phrase)
    except Exception as e:
        logger.error(f"Failed to initialize blockchain: {e}")
        st.error("❌ Failed to initialize blockchain. Check your secrets configuration.")
        return None

class Scene:
    def __init__(self, key: str, description: str, choices: Dict[str, str]):
        self.key = key
        self.description = description
        self.choices = choices

# Define scenes
scenes = {
    "intro": Scene(
        "intro",
        "🧙 You awaken in a moss-covered stone circle. Fog drips from twisted trees. A raven stares.\n"
        "Your only belongings: a rusty dagger, a torn map, and a faint headache that feels... cursed.",
        {
            "Examine the map": "map_scene",
            "Talk to the raven": "raven_scene",
            "Walk into the forest": "forest_path"
        }
    ),
    "map_scene": Scene(
        "map_scene",
        "📜 The map shows a ruin labeled 'Whispering Vault' and a trail marked with cryptic runes.",
        {
            "Follow the trail": "forest_path",
            "Return to the stone circle": "intro"
        }
    ),
    "raven_scene": Scene(
        "raven_scene",
        "🪶 The raven cocks its head. In a raspy human voice it says: 'Three paths, one truth. Don't trust the smiling god.'",
        {
            "Demand more answers": "raven_mystery",
            "Back away slowly": "intro"
        }
    ),
    "raven_mystery": Scene(
        "raven_mystery",
        "🦉 The raven screeches and bursts into black feathers. A silver key is left behind.",
        {
            "Take the key and head to the forest": "forest_path"
        }
    ),
    "forest_path": Scene(
        "forest_path",
        "🌲 The forest path splits ahead. One way leads to light and laughter. The other, to silence and cold shadows.",
        {
            "Take the bright path": "bright_path",
            "Take the dark path": "dark_path"
        }
    ),
    "bright_path": Scene(
        "bright_path",
        "🌞 Warm light filters through golden leaves. You hear music, distant and cheerful. A small cottage lies ahead.\n"
        "An old man sits outside, whittling a flute from bone. His smile doesn't reach his eyes.",
        {
            "Speak to the old man": "light_mystery",
            "Ignore him and walk past": "END"
        }
    ),
    "dark_path": Scene(
        "dark_path",
        "🌑 The air grows colder. Trees groan like dying things. You find a ruined shrine where an old man in rags tends a flickering blue flame.\n"
        "His eyes are milky, but he speaks before you do: 'I saw you in the ashes.'",
        {
            "Ask what he means": "dark_mystery",
            "Back away into the forest": "END"
        }
    ),
    "light_mystery": Scene(
        "light_mystery",
        "🎵 The old man chuckles. 'So you've heard the laughter too. Most think it's the fairfolk — it's not.'\n"
        "'The Whispering Vault opens soon. When it does, not even gods will sleep safe.'",
        {
            "Ask about the Whispering Vault": "END"
        }
    ),
    "dark_mystery": Scene(
        "dark_mystery",
        " The blind man dips his finger into the blue flame and draws a sigil in the air. It burns into your vision.\n"
        "'You were marked at birth. The Vault remembers. And it waits.'",
        {
            "Stare into the flame": "END"
        }
    )
}

class StreamlitGame:
    def __init__(self):
        # Initialize blockchain with seed phrase from secrets
        self.blockchain = initialize_blockchain()
        
        # Initialize session state if not already done
        if 'current_scene_key' not in st.session_state:
            st.session_state.current_scene_key = "intro"
        
        if 'game_ended' not in st.session_state:
            st.session_state.game_ended = False

    def display_scene(self, scene: Scene):
        # Display scene description
        st.markdown(f"## {scene.description}")

        # Display choices
        st.markdown("### What do you do?")
        
        # Create choice buttons
        for choice_text, next_scene_key in scene.choices.items():
            if st.button(choice_text, key=f"choice_{next_scene_key}"):
                if next_scene_key == "END":
                    st.session_state.game_ended = True
                    st.session_state.current_scene_key = "intro"
                else:
                    st.session_state.current_scene_key = next_scene_key
                st.rerun()

    def display_save_load_buttons(self):
        """Display save and load buttons at the bottom"""
        if not self.blockchain:
            st.error("💡 Save/Load functionality unavailable - blockchain not initialized")
            return

        st.markdown("---")
        
        # Create two columns for save/load buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Game", key="save_button"):
                if self.blockchain.save_game(st.session_state.current_scene_key):
                    st.success("✅ Progress saved!")
                else:
                    st.error("❌ Failed to save progress")
                    
        with col2:
            if st.button("📂 Load Game", key="load_button"):
                saved_scene_key = self.blockchain.load_game()
                if saved_scene_key and saved_scene_key in scenes:
                    st.session_state.current_scene_key = saved_scene_key
                    st.success("✅ Progress loaded!")
                    st.rerun()
                else:
                    st.error("❌ No saved progress found")

def main():
    # Title
    st.title("🎮 Choose Your Own Adventure")
    
    # Initialize game
    game = StreamlitGame()
    
    try:
        # Check if game has ended
        if st.session_state.game_ended:
            st.markdown("## 🔚 Your journey ends here. For now...")
            if st.button("Start New Game"):
                st.session_state.game_ended = False
                st.session_state.current_scene_key = "intro"
                st.rerun()
        else:
            # Display current scene and choices
            current_scene = scenes[st.session_state.current_scene_key]
            game.display_scene(current_scene)
            
            # Add some space before the save/load buttons
            st.markdown("<br>" * 2, unsafe_allow_html=True)
            
            # Display save/load buttons at the bottom
            game.display_save_load_buttons()
        
        # Add a footer
        st.markdown("---")
        st.markdown("*A blockchain-powered adventure game*")
        
    except Exception as e:
        logger.error(f"Error in game: {str(e)}")
        st.error("❌ Something went wrong. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Game crashed: {str(e)}")
        st.error("❌ An error occurred. Check cyoa_game.log for details.")
