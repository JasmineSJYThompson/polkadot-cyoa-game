from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

import time

console = Console()

# Scene definitions
scenes = {
    "start_city_edge": {
        "desc": "You awaken near a derelict district of UrukCorp sprawl. Drones swarm nearby. Your implant buzzes—someone wants you dead.",
        "choices": {
            "Flee into the slums": "slum_encounter_enkidu",
            "Fight the drones": "corp_response_chase"
        }
    },
    "slum_encounter_enkidu": {
        "desc": "You meet Enkidu, a synthetic runaway with corrupted memory. He claims he knew you before you were rebuilt.",
        "choices": {
            "Help Enkidu hide": "abandoned_subnet_hideout",
            "Report Enkidu": "siduri_offer_contact"
        }
    },
    "corp_response_chase": {
        "desc": "Fighting draws attention. A CorpSec pursuit triggers a lockdown. You must escape.",
        "choices": {
            "Escape through maintenance": "abandoned_subnet_hideout",
            "Call for help": "siduri_offer_contact"
        }
    },
    "abandoned_subnet_hideout": {
        "desc": "In the depths of the net, Enkidu shows you fragments of the Dilmun Protocol. You recall flashes of your past.",
        "choices": {
            "Investigate memory": "core_memory_node_access",
            "Question Enkidu": "enkidu_trust_build"
        }
    },
    "siduri_offer_contact": {
        "desc": "Siduri offers you information in exchange for memory fragments or loyalty. She knows about Dilmun.",
        "choices": {
            "Trade memory": "siduri_trust_build",
            "Refuse trade": "enkidu_warns_you"
        }
    },
    "core_memory_node_access": {
        "desc": "You unlock a buried memory node—an image of a younger Enkidu, calling you 'King'. Your past is rewriting itself.",
        "choices": {
            "Dig deeper": "first_augmentation_offer",
            "Shut it down": "enkidu_trust_build"
        }
    },
    "enkidu_trust_build": {
        "desc": "Enkidu opens up about his fears. He believes you’re becoming someone else. You bond—or don’t.",
        "choices": {
            "Promise him trust": "first_augmentation_offer",
            "Deflect with joke": "siduri_trust_build"
        }
    },
    "siduri_trust_build": {
        "desc": "Siduri tests your willingness to cut ethical corners. She offers you an augment.",
        "choices": {
            "Accept augment": "first_augmentation_implant",
            "Decline augment": "corp_ambush_encounter"
        }
    },
    "enkidu_warns_you": {
        "desc": "Enkidu warns Siduri will twist your mind. Trust between them fractures. You feel the tension.",
        "choices": {
            "Side with Enkidu": "first_augmentation_offer",
            "Side with Siduri": "first_augmentation_implant"
        }
    },
    "first_augmentation_offer": {
        "desc": "An AI surgeon offers you augmentations—tools for survival, but at a cost to your humanity.",
        "choices": {
            "Install mind augment": "corp_ambush_encounter",
            "Install skin augment": "corp_ambush_encounter",
            "Refuse all": "corp_ambush_encounter"
        }
    },
    "first_augmentation_implant": {
        "desc": "Pain pulses through you. Your thoughts race, but a piece of yourself feels missing.",
        "choices": {
            "Reconnect with Enkidu": "data_shard_heist_plan",
            "Follow Siduri's plan": "data_shard_heist_plan"
        }
    },
    "corp_ambush_encounter": {
        "desc": "CorpSec ambushes you mid-journey. Enkidu defends you, gets wounded. Siduri watches, calculating.",
        "choices": {
            "Rescue Enkidu": "data_shard_heist_plan",
            "Leave Enkidu": "data_shard_heist_plan"
        }
    },
    "data_shard_heist_plan": {
        "desc": "You plan to steal the Seed of Origin—a digital DNA file linked to resurrection protocols. You need both allies.",
        "choices": {
            "Infiltrate alone": "data_shard_heist",
            "Go with team": "data_shard_heist"
        }
    },
    "data_shard_heist": {
        "desc": "You penetrate a GodCorp archive. Enkidu saves you from lethal ICE. Siduri extracts the data shard.",
        "choices": {
            "Hand data to Siduri": "act_one_end_siduri_path",
            "Give data to Enkidu": "act_one_end_enkidu_path"
        }
    },
    "act_one_end_siduri_path": {
        "desc": "Siduri takes the shard, promising power. Enkidu watches, silent. She says it’s time to leave the city.",
        "choices": {
            "Leave Uruk": "act_two_start"
        }
    },
    "act_one_end_enkidu_path": {
        "desc": "Enkidu holds the shard. “This could save us,” he says. Siduri vanishes. He asks you to trust him one more time.",
        "choices": {
            "Leave Uruk": "act_two_start"
        }
    },
    "act_two_start": {
        "desc": "To be continued in Act II..."
    }
}

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
            console.print(f"[bold magenta]{i}.[/bold magenta] {choice}")
        
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

