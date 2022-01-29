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
       
            data = response.get_json()
            game_id = data['game_id']
            board = data['board']
  
            self.assertTrue(game_id)
            self.assertTrue(board)
            self.assertTrue(games)

    def test_api_score_word(self):
        """ Test trying to score a word (valid only) """
        with self.client as client:

            game_id = client.post("/api/new-game").get_json()['game_id']
            game = games[game_id]

            game.board[0] = ["C", "A", "X", "X", "X"]
            game.board[1] = ["X", "T", "X", "X", "X"]
            game.board[2] = ["D", "O", "G", "X", "X"]
            game.board[3] = ["X", "X", "X", "X", "X"]
            game.board[4] = ["X", "X", "X", "X", "X"]

            response = self.client.post(
                "/api/score-word",
                json={"word": "CAT", "gameId": game_id})
            self.assertEqual(response.get_json(), {'result': 'ok'})