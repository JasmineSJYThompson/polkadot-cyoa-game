from django.urls import path
from . import views
from .views import GameListView, GameDetailView

urlpatterns = [
    # Regular game-related paths
    path('select/', views.game_select_view, name='game_select'),           # <-- FIRST
    path('play/<int:game_id>/', views.start_game_view, name='start_game'), # <-- THEN THIS
    path('', views.game_select_view, name='game_list'),                   # <-- THEN THIS

    # API game-related paths
    path('api/games/', GameListView.as_view(), name='game_list'),
    path('api/games/<int:game_id>/', GameDetailView.as_view(), name='game_detail'),

    # Catch-all for scene navigation
    path('<str:scene_id>/', views.show_scene, name='scene'),               # <-- CATCH-ALL LAST
]

