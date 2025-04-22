from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import time
import json
import os
import sys

console = Console()

# Determine if we're in developer mode
DEVELOPER_MODE = "--dev" in sys.argv

# Scene definitions
scenes = {}
with open("json_files/scenes.json", "r") as f:
    scenes = json.load(f)["scenes"]

def type_out(text, delay=0.02):
    """Types out the text with a slight delay unless in dev mode."""
    if DEVELOPER_MODE:
        console.print(text, style="cyan", soft_wrap=True)
    else:
        for char in text:
            console.print(char, end='', style="cyan", soft_wrap=True)
            time.sleep(delay)
        console.print()  # for newline

def display_image_ascii(scene_name):
    """Load ASCII art from file and print it to the console."""
    ascii_path = f"ascii_art/{scene_name}.asc"
    if os.path.exists(ascii_path):
        with open(ascii_path, 'r', encoding='utf-8') as file:
            ascii_art = file.read()
            console.print(ascii_art)
    else:
        console.print("[bold red]No ASCII art found for this scene.[/bold red]")

def get_scene_description(scene_name):
    scene_file = f"scenes/{scene_name}.txt"
    if os.path.exists(scene_file):
        with open(scene_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "[bold red]Scene description not found.[/bold red]"

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import time
import json
import os
import sys

console = Console()

# Determine if we're in developer mode
DEVELOPER_MODE = "--dev" in sys.argv

# Scene definitions
scenes = {}
with open("json_files/scenes.json", "r") as f:
    scenes = json.load(f)["scenes"]

def type_out(text, delay=0.02):
    """Types out the text with a slight delay unless in dev mode."""
    if DEVELOPER_MODE:
        console.print(text, style="cyan", soft_wrap=True)
    else:
        for char in text:
            console.print(char, end='', style="cyan", soft_wrap=True)
            time.sleep(delay)
        console.print()  # for newline

def display_image_ascii(scene_name):
    """Load ASCII art from file and print it to the console."""
    ascii_path = f"ascii_art/{scene_name}.asc"
    if os.path.exists(ascii_path):
        with open(ascii_path, 'r', encoding='utf-8') as file:
            ascii_art = file.read()
            console.print(ascii_art)
    else:
        console.print("[bold red]No ASCII art found for this scene.[/bold red]")

def get_scene_description(scene_name):
    scene_file = f"scenes/{scene_name}.txt"
    if os.path.exists(scene_file):
        with open(scene_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "[bold red]Scene description not found.[/bold red]"

def play_game():
    current = "start_city_edge"
    history = []

    while True:
        console.clear()
        scene = scenes[current]  # ← This was missing!

        if DEVELOPER_MODE:
            console.print(Panel.fit(f"[bold red]{current}[/bold red] [green](Dev Mode)[/green]"))
            short_desc = scene.get("desc", "[italic grey]No short description found in scenes.json[/italic grey]")
            console.print(f"[green]{short_desc}\n[/green]")
        else:
            console.print(Panel.fit(f"[bold red]{current}[/bold red]"))

        # Show the description with appropriate timing
        desc_text = get_scene_description(current)
        type_out(desc_text)
        if not DEVELOPER_MODE:
            time.sleep(1)

        display_image_ascii(current)

        if "choices" not in scene:
            console.print("\n[bold green]>> End of this path. Type 'restart' to begin again.[/bold green]")
            cmd = Prompt.ask("\n[bold yellow]>>[/bold yellow]").strip().lower()
            if cmd == "restart":
                current = "start_city_edge"
                history.clear()
            continue

        options = list(scene["choices"].keys())
        for i, choice in enumerate(options, 1):
            parts = choice.replace("_", " ").split()
            if parts:
                parts[0] = parts[0].capitalize()
            formatted_choice = " ".join(parts)
            console.print(f"[bold magenta]{i}.[/bold magenta] {formatted_choice}")
        
        while True:
            if DEVELOPER_MODE:
                cmd = Prompt.ask("\n[bold yellow]Choose an option (or type 'restart', 'back' or 'exit')[/bold yellow]").strip().lower()
                if cmd == "back":
                    if history:
                        current = history.pop()
                        break
                    else:
                        console.print("[bold red]No previous scene to go back to.[/bold red]")
            else:
                cmd = Prompt.ask("\n[bold yellow]Choose an option (or type 'restart' or 'exit')[/bold yellow]").strip().lower()
            if cmd == "restart":
                current = "start_city_edge"
                history.clear()
                break
            elif cmd == "exit":
                quit()
            elif cmd.isdigit() and 1 <= int(cmd) <= len(options):
                history.append(current)
                current = scene["choices"][options[int(cmd)-1]]
                break
            else:
                console.print("[bold red]Invalid input.[/bold red] Try again.")

if __name__ == "__main__":
    play_game()

