from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Game

class GameApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()  # Initialize the client
        self.user = User.objects.create_user(username='testuser', password='password')  # Create a test user
        self.client.login(username='testuser', password='password')  # Login the user
        self.game = Game.objects.create(title="Sample Game", description="A fun game.")  # Create test data
    
    def test_get_games(self):
        response = self.client.get('/api/games/')  # Send GET request to /api/games
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check for 200 OK response
        self.assertEqual(len(response.data), 1)  # Assuming it returns 1 game (adjust based on your data)
        self.assertEqual(response.data[0]['title'], 'Sample Game')  # Check the title field

