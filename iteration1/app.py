# app.py

import streamlit as st
from blockchain_storage import BlockchainStorage
import logging

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
        print("❌ Failed to initialize blockchain. Check your secrets configuration.")
        return None

class Scene:
    def __init__(self, key, description, choices):
        self.key = key  # Unique identifier for the scene
        self.description = description  # Text shown to the player
        self.choices = choices  # Dict of {choice_text: next_scene_key}

    def display(self):
        print(f"\n{self.description}\n")
        for idx, choice in enumerate(self.choices.keys(), 1):
            print(f"{idx}. {choice}")
        print("\nSpecial commands: 'SAVE' to save progress, 'LOAD' to load last save")

    def get_next_scene_key(self, choice_number):
        if 1 <= choice_number <= len(self.choices):
            return list(self.choices.values())[choice_number - 1]
        else:
            return None

# === Define your world here ===
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
        "🕯 The blind man dips his finger into the blue flame and draws a sigil in the air. It burns into your vision.\n"
        "'You were marked at birth. The Vault remembers. And it waits.'",
        {
            "Stare into the flame": "END"
        }
    )
}

class Game:
    def __init__(self, scenes, start_scene_key):
        self.scenes = scenes
        self.current_scene = scenes[start_scene_key]
        self.blockchain = initialize_blockchain()

    def run(self):
        while True:
            self.current_scene.display()
            try:
                choice = input("\nWhat do you do? Choose a number or type 'SAVE'/'LOAD': ").strip().upper()
                
                # Handle save command
                if choice == 'SAVE':
                    if self.blockchain and self.blockchain.save_game(self.current_scene.key):
                        print("✅ Progress saved!")
                    else:
                        print("❌ Failed to save progress")
                    continue
                
                # Handle load command
                elif choice == 'LOAD':
                    if self.blockchain:
                        saved_scene_key = self.blockchain.load_game()
                        if saved_scene_key and saved_scene_key in self.scenes:
                            self.current_scene = self.scenes[saved_scene_key]
                            print("✅ Progress loaded!")
                        else:
                            print("❌ No saved progress found")
                    else:
                        print("❌ Blockchain not initialized")
                    continue
                
                # Handle normal game choices
                try:
                    choice_num = int(choice)
                    next_key = self.current_scene.get_next_scene_key(choice_num)
                    if next_key is None:
                        print("❌ Invalid choice. Try again.")
                    elif next_key == "END":
                        print("\n🔚 Your journey ends here. For now...")
                        break
                    else:
                        self.current_scene = self.scenes[next_key]
                except ValueError:
                    print("❌ Please enter a valid number or type 'SAVE'/'LOAD'")
            except Exception as e:
                logger.error(f"Error in game loop: {str(e)}")
                print("❌ Something went wrong. Please try again.")

if __name__ == "__main__":
    try:
        logger.info("Starting game...")
        game = Game(scenes, "intro")
        game.run()
    except Exception as e:
        logger.error(f"Game crashed: {str(e)}")
        print("❌ An error occurred. Check cyoa_game.log for details.")
