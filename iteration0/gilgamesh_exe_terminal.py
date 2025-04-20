from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

import time
import json

console = Console()

# Scene definitions
scenes = {}
with open("scenes.json", "r") as f:
    scenes = json.load(f)["scenes"]

def type_out(text, delay=0.02):
    for char in text:
        console.print(char, end='', style="cyan", soft_wrap=True)
        time.sleep(delay)
    console.print()  # for newline

def play_game():
    current = "start_city_edge"
    while True:
        console.clear()
        scene = scenes[current]
        console.print(Panel.fit(f"[bold red]{current}[/bold red]"))
        type_out(scene["desc"])
        time.sleep(1)  # Small delay before showing options
        
        if "choices" not in scene:
            console.print("\n[bold green]>> End of this path. Type 'restart' to begin again.[/bold green]")
            cmd = Prompt.ask("\n[bold yellow]>>[/bold yellow]").strip().lower()
            if cmd == "restart":
                current = "start_city_edge"
            continue

        options = list(scene["choices"].keys())
        for i, choice in enumerate(options, 1):
            formatted_choice = choice.replace("_", " ")
            console.print(f"[bold magenta]{i}.[/bold magenta] {formatted_choice}")
        
        while True:
            cmd = Prompt.ask("\n[bold yellow]Choose an option (or type 'restart')[/bold yellow]").strip().lower()
            if cmd == "restart":
                current = "start_city_edge"
                break
            if cmd.isdigit() and 1 <= int(cmd) <= len(options):
                current = scene["choices"][options[int(cmd)-1]]
                break
            else:
                console.print("[bold red]Invalid input.[/bold red] Try again.")

if __name__ == "__main__":
    play_game()

