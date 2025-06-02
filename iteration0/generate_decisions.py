from pathlib import Path
from langchain_core.messages import HumanMessage
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load .env and get GOOGLE_API_KEY
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

def load_scene_text(scene_key: str, scenes_dir: str = "scenes") -> str:
    path = Path(scenes_dir) / f"{scene_key}.txt"
    return path.read_text(encoding="utf-8").strip()

def summarize_scene(scene_text: str, scene_name: str, llm) -> str:
    prompt = HumanMessage(content=textwrap.dedent(f"""
        You are summarizing a scene from an interactive fiction game. Summarize the key plot beats in 3-5 sentences. Do NOT add any new characters or plot developments.

        Scene Name: {scene_name}
        Scene Text:
        {scene_text}
    """))

    response = llm.invoke([prompt])
    return response.content.strip()

def generate_decision_text(decision_name: str, scene_from: str, scene_to: str, llm) -> str:
    print(f"[INFO] Loading scenes: {scene_from} -> {scene_to}")
    text_from = load_scene_text(scene_from)
    text_to = load_scene_text(scene_to)

    print("[INFO] Summarizing scene_from...")
    summary_from = summarize_scene(text_from, scene_from, llm)
    print("[INFO] Summarizing scene_to...")
    summary_to = summarize_scene(text_to, scene_to, llm)

    # Save summarized scenes
    summarized_scenes_dir = Path("summarized_scenes")
    summarized_scenes_dir.mkdir(parents=True, exist_ok=True)
    
    summary_from_path = summarized_scenes_dir / f"{scene_from}.txt"
    summary_from_path.write_text(summary_from, encoding="utf-8")
    print(f"[INFO] Saved summarized scene: {scene_from} -> {summary_from_path}")

    summary_to_path = summarized_scenes_dir / f"{scene_to}.txt"
    summary_to_path.write_text(summary_to, encoding="utf-8")
    print(f"[INFO] Saved summarized scene: {scene_to} -> {summary_to_path}")

    bridge_prompt = HumanMessage(content=textwrap.dedent(f"""
        You are writing a branching narrative transition for a game. 
        The player has made a choice: '{decision_name}'.
        You are to write a short interactive fiction scene that logically connects these two narrative summaries.

        FROM SCENE SUMMARY:
        {summary_from}

        TO SCENE SUMMARY:
        {summary_to}

        Write a short 100 word scene that leads from the first summary to the second. 
        Do NOT introduce any major new events or characters. 
        Your job is to make the transition feel seamless and emotionally grounded.
    """))

    print("[DEBUG] Prompt length:", len(bridge_prompt.content))
    print("[INFO] Generating decision transition for:", decision_name)
    result = llm.invoke([bridge_prompt])
    return result.content.strip()

def main():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.5,
        max_tokens=300,
        google_api_key=GOOGLE_API_KEY,
    )

    while True:
        decision_name = input("Enter decision name (or 'exit' to quit): ").strip()
        if decision_name == "exit":
            break
        scene_from = input("Enter scene FROM (exact key, no file extension): ").strip()
        scene_to = input("Enter scene TO (exact key, no file extension): ").strip()

        decision_text = generate_decision_text(decision_name, scene_from, scene_to, llm)

        print("\n=== Decision Bridge ===\n")
        print(decision_text)

        # Save to file
        output_dir = Path("decisions")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{decision_name}.txt"
        output_path.write_text(decision_text, encoding="utf-8")
        print(f"\n[INFO] Saved decision bridge to {output_path}")

if __name__ == "__main__":
    main()