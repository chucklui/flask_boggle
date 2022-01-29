from unittest import TestCase
from flask import request
from app import app, games
import json

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form id="newWordForm">', html)
            self.assertIn('<table class="board">', html)

            # For later use when we want to check the session data
            # self.assertEqual(session[STRING],VALUE)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            data = json.loads(response.get_data(as_text=True))
            self.assertTrue(data['game_id'])
            self.assertTrue(data['board'])
            self.assertTrue(games)

    def test_api_score_word(self):
        """ Test trying to score a word (valid only) """
        with self.client as client:

            game_id = client.post("/api/new-game").get_json()['gameId']
            game = games[game_id]

            response = client.post('/api/score-word')



            data = json.loads(response.get_data(as_text=True))