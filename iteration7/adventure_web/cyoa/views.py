import json
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Game

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import GameSerializer

# Load the JSON file once
with open("cyoa/scenes.json", "r") as f:
    STORY = json.load(f)["scenes"]

@login_required
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

@login_required
def game_select_view(request):
    games = Game.objects.all()
    return render(request, 'game_select.html', {'games': games})


@login_required
def start_game_view(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game not found")

    # For now, just redirect to the default scene (can later be game-specific)
    return redirect('scene', scene_id='start_city_edge')

class GameListView(LoginRequiredMixin, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

class GameDetailView(LoginRequiredMixin, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, game_id):
        game = Game.objects.get(id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('/')  # Redirect to the home page (or any other page after login)
        else:
            # If authentication fails, show an error message
            return render(request, "login.html", {"error": "Invalid credentials. Please try again."})
    
    return render(request, "login.html")

