import requests
from random import sample
from flask import Flask, jsonify
from fetcher import Fetcher

app = Flask(__name__)
favorites = Fetcher(requests)


@app.get('/favorite_pokemon')
def list_favorite_pokemon():
    return jsonify([name for name in favorites.favorites().keys()])


@app.get('/favorite_pokemon/<pokemon>')
def get_favorite_pokemon(pokemon):
    data = favorites.favorites().get(pokemon)
    if data is None:
        return 'Sorry, that one just does not make the cut', 404
    favorite = data.copy()
    # We want to just display 2 random moves.
    favorite['moves'] = [move['move']['name'] for move in sample(favorite['moves'], k=2)]
    return jsonify(favorite)
