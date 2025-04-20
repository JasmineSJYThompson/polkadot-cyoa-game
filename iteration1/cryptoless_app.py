# app.py

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

class Scene:
    def __init__(self, key, description, choices):
        self.key = key  # Unique identifier for the scene
        self.description = description  # Text shown to the player
        self.choices = choices  # Dict of {choice_text: next_scene_key}

    def display(self):
        print(f"\n{self.description}\n")
        for idx, choice in enumerate(self.choices.keys(), 1):
            print(f"{idx}. {choice}")
        print("\nType 'R' to restart the game")

    def get_next_scene_key(self, choice_number):
        if 1 <= choice_number <= len(self.choices):
            return list(self.choices.values())[choice_number - 1]
        else:
            return None

# Raw scenes data
raw_scenes = {
    "intro": {
        "key": "intro",
        "description": "👑 You are Gilgamesh, King of Uruk. Half god, half man. Restless, unmatched. Your people whisper prayers... and curses.",
        "choices": {
            "Walk the streets of Uruk": "uruk_streets",
            "Visit the temple of Ishtar": "ishtar_temple"
        }
    },
    "uruk_streets": {
        "key": "uruk_streets",
        "description": "🏛️ Uruk's walls tower above. Merchants haggle, children run. A beggar pulls your robe.",
        "choices": {
            "Ignore him": "ignore_beggar",
            "Listen to his plea": "beggar_warning"
        }
    },
    "ishtar_temple": {
        "key": "ishtar_temple",
        "description": "🔥 Inside Ishtar's temple, incense burns. Priestesses chant. The goddess stirs in her shrine.",
        "choices": {
            "Offer a prayer": "ishtar_prayer",
            "Demand a vision": "ishtar_demand"
        }
    },
    "ignore_beggar": {
        "key": "ignore_beggar",
        "description": "🧍‍♂️ You walk past the beggar. The people watch in silence.",
        "choices": {
            "Return to your palace": "palace_return",
            "Challenge a warrior to duel": "duel_scene"
        }
    },
    "beggar_warning": {
        "key": "beggar_warning",
        "description": "🌾 The beggar warns: 'A wild man roams the hills. Your equal.'",
        "choices": {
            "Seek this wild man": "seek_enkidu",
            "Dismiss him": "dismiss_warning"
        }
    },
    "ishtar_prayer": {
        "key": "ishtar_prayer",
        "description": "🕯️ You kneel. Ishtar whispers: 'Soon, you'll face yourself.'",
        "choices": {
            "Ask for clarity": "ishtar_clarity",
            "Leave in silence": "temple_exit"
        }
    },
    "ishtar_demand": {
        "key": "ishtar_demand",
        "description": "🌬️ You shout. A breeze chills your spine. No answer.",
        "choices": {
            "Leave": "temple_exit",
            "Smash the altar": "ishtar_curse"
        }
    },
    "palace_return": {
        "key": "palace_return",
        "description": "🏰 The palace welcomes you with golden stone and tired advisors.",
        "choices": {
            "Hold court": "hold_court",
            "Retreat to your chambers": "rest_scene"
        }
    },
    "duel_scene": {
        "key": "duel_scene",
        "description": "⚔️ A scarred soldier accepts. The crowd gathers.",
        "choices": {
            "Strike first": "strike_first",
            "Let him attack": "wait_defend"
        }
    },
    "seek_enkidu": {
        "key": "seek_enkidu",
        "description": "🌄 You head to the wildlands. Tracks lead to the river.",
        "choices": {
            "Follow the tracks": "river_tracks",
            "Wait by the water": "river_wait"
        }
    },
    "dismiss_warning": {
        "key": "dismiss_warning",
        "description": "🔥 You laugh. The beggar vanishes. That night, your dreams burn with fire.",
        "choices": {
            "Interpret dream": "dream_scene",
            "Ignore it": "dream_ignore"
        }
    },
    "ishtar_clarity": {
        "key": "ishtar_clarity",
        "description": "💫 'He is you, yet not you,' whispers Ishtar. 'Choose how you meet him.'",
        "choices": {
            "With fists": "meet_with_fists",
            "With food": "meet_with_food"
        }
    },
    "temple_exit": {
        "key": "temple_exit",
        "description": "🦅 You leave the temple. A hawk circles overhead.",
        "choices": {
            "Return to the palace": "palace_return",
            "Seek omens in the hills": "seek_omens"
        }
    },
    "ishtar_curse": {
        "key": "ishtar_curse",
        "description": "⚡ The altar cracks. Lightning splits the sky. A curse now follows you.",
        "choices": {
            "Embrace it": "curse_embrace",
            "Seek forgiveness": "seek_forgiveness"
        }
    }
}

# Convert raw scenes to Scene objects
scenes = {
    key: Scene(data["key"], data["description"], data["choices"])
    for key, data in raw_scenes.items()
}

class Game:
    def __init__(self, scenes, start_scene_key):
        self.scenes = scenes
        self.current_scene = scenes[start_scene_key]
        self.start_scene_key = start_scene_key  # Store the starting scene key

    def restart(self):
        """Reset the game to the starting scene"""
        self.current_scene = self.scenes[self.start_scene_key]
        print("\n🔄 Restarting game...\n")

    def run(self):
        while True:
            self.current_scene.display()
            try:
                choice = input("\nWhat do you do? Choose a number or 'R' to restart: ").strip().upper()
                
                # Handle restart command
                if choice == 'R':
                    self.restart()
                    continue
                
                try:
                    choice_num = int(choice)
                    next_key = self.current_scene.get_next_scene_key(choice_num)
                    if next_key is None:
                        print("❌ Invalid choice. Try again.")
                    elif next_key == "END":
                        print("\n🔚 Your journey ends here. For now...")
                        # Ask if they want to restart
                        while True:
                            restart = input("\nWould you like to restart? (Y/N): ").strip().upper()
                            if restart == 'Y':
                                self.restart()
                                break
                            elif restart == 'N':
                                return  # Exit the game
                            else:
                                print("Please enter Y or N")
                    elif next_key not in self.scenes:
                        print("⚠️ That path is not yet written. Try another choice.")
                    else:
                        self.current_scene = self.scenes[next_key]
                except ValueError:
                    print("❌ Please enter a valid number or 'R' to restart")
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