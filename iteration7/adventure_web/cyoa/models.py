from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_scene = models.CharField(max_length=255, default="start_city_edge")

    def __str__(self):
        return self.title

class Scene(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    scene_id = models.CharField(max_length=100)
    text = models.TextField()
    choices = models.JSONField()  # or use a related model if you want structure