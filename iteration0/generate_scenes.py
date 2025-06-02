import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# Load .env and get GOOGLE_API_KEY
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Load JSON context files
def load_json_context():
    context = {}
    for filename in ["characters.json", "orgs.json", "scenes.json", "synopsis.json"]:
        with open(f"./json_files/{filename}", "r", encoding="utf-8") as f:
            context[filename.replace(".json", "")] = json.load(f)
    return context

# Generate prompt for a scene
def build_scene_prompt(scene_key, context):
    scene_data = context["scenes"]["scenes"][scene_key]
    synopsis = context["synopsis"]
    characters = context["characters"]

    return f"""You are a cyberpunk screenwriter collaborating with an AI. 
Write a vivid, immersive scene for a visual novel based on the following:

### Scene Name
{scene_key}

### Scene Description
{scene_data['desc']}

### Scene Choices
{scene_data.get('choices', {})}

### World & Narrative Context
{synopsis}

### Key Characters
{json.dumps(characters, indent=2)}

Write the scene as a short, compelling prose segment with embedded dialogue.
Only write the lead-in narrative before any choices. Do NOT include the choices.
"""

# Run LLM scene generation using Gemini
def generate_scene(scene_key, context):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
        max_output_tokens=500,
        convert_system_message_to_human=True
    )
    
    prompt_text = build_scene_prompt(scene_key, context)
    messages = [
        SystemMessage(content="You are a narrative designer for a cyberpunk visual novel."),
        HumanMessage(content=prompt_text)
    ]
    
    result = llm.invoke(messages)
    return result.content

# Save generated scene
def save_scene(scene_key, scene_text):
    os.makedirs("./scenes", exist_ok=True)
    with open(f"./scenes/{scene_key}.txt", "w", encoding="utf-8") as f:
        f.write(scene_text)

# Main loop
def main():
    context = load_json_context()

    while True:
        scene_key = input("Enter exact scene name (or 'exit' to quit): ").strip()
        if scene_key.lower() == "exit":
            print("Exiting.")
            break

        if scene_key not in context["scenes"]["scenes"]:
            print(f"Scene '{scene_key}' not found. Try again.")
            continue

        print(f"Generating scene: {scene_key} ...")
        scene_text = generate_scene(scene_key, context)
        save_scene(scene_key, scene_text)
        print(f"Scene '{scene_key}' saved to ./scenes/{scene_key}.txt\n")

if __name__ == "__main__":
    main()
