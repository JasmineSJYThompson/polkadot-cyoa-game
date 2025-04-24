from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_scene, name='start'),
    path('<str:scene_id>/', views.show_scene, name='scene'),
]

