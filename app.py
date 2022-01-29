from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.board

    return jsonify(game_id=game_id, board=board)

@app.post("/api/score-word")
def score_word():
    """ We take a word and check its validity for scoring. """

    # breakpoint()
    game_id = request.json["gameId"]
    word = request.json["word"].upper()

    is_word_value = games[game_id].is_word_in_word_list(word)
    check_word_value = games[game_id].check_word_on_board(word)
    # breakpoint()

    if not is_word_value:
        return jsonify({"result": "not-word"})
    if not check_word_value:
        return jsonify({"result": "not-on-board"})
    if is_word_value and check_word_value:
        return jsonify({"result": "ok"})

