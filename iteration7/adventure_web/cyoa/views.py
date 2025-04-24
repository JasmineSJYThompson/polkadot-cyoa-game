import json
from django.shortcuts import render
from django.http import Http404

# Load the JSON file once
with open("cyoa/scenes.json", "r") as f:
    STORY = json.load(f)["scenes"]

def show_scene(request, scene_id="start_city_edge"):
    scene = STORY.get(scene_id)
    if not scene:
        raise Http404("Scene not found")

    # Pre-process choices to format labels nicely
    formatted_choices = {
        label.replace('_', ' ').capitalize(): target
        for label, target in scene["choices"].items()
    }

    return render(request, "cyoa/scene.html", {"scene_id": scene_id, "scene": scene, "choices": formatted_choices})

