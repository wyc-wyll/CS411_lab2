from __future__ import annotations

import flask
import time
from flask_cors import CORS
from model import ConcentrationModel

app = flask.Flask(__name__)
CORS(app)

model = ConcentrationModel()

guess_count = 0

def evaluate(i1: int, i2:int):
    global guess_count
    guess_count += 1

    if (model.cards[i1][0] == model.cards[i2][0]):
        model.matched[i1] = True
        model.matched[i2] = True


@app.route('/health', methods=['GET'])
def health() -> flask.Response:
    """Health check.

    """
    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@app.route('/reset', methods=['POST'])
def reset() -> flask.Response:
    """Reset game.

    """
    # Specify global scope if going to change the value of a global variable.
    
    global model
    global guess_count

    model = ConcentrationModel()

    guess_count = 0

    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@app.route('/card/<int:index>', methods=['GET'])
def card(index: int) -> flask.Response:
    """Get card info.

    Parameter
    ---------
    index : int
        The card's index

    """
    # TODO: Implement. See Part 2: Card information.
    data = {
        "card": model.cards[index],
        "match": model.matched[index],
        "state": model.state[index]
    }

    return flask.make_response(data, 200)


@app.route('/select/<int:index>', methods=['POST'])
def select(index: int) -> flask.Response:
    """Select a card.

    """
    # Specify global scope if going to change the value of a global variable.
    global model
    global guess_count
    # Edge cases: Selecting a matched card or selected card.
    if model.matched[index] is True:
        data = {
            'message': 'Card already matched. Try again.'
        }
        return flask.make_response(data, 200)
    if model.state[index] == 'up':
        data = {
            'message': 'Card already selected. Try again.'
        }
        return flask.make_response(data, 200)

    # TODO: Implement. See Part 3: Card selection.
    model.state[index] = 'up'
    for i in range(1, len(model.cards)):
        if model.matched[i]:
            continue

        if i != index and model.state[i] == "up":
            evaluate(i, index)
            break
    

    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@app.route('/guesses', methods=['GET'])
def get_guesses() -> flask.Response:
    """Get number of guesses.

    """
    global guess_count
    # TODO: Implement. See Part 4: Guesses counter.

    data = {
        "guesses": guess_count
    }

    return flask.make_response(data, 200)

@app.route('/flip', methods=['POST'])
def flip() -> flask.Response:
    time.sleep(3) # for last visualization
    index = -1
    for i in range(1, len(model.cards)):
        if model.state[i] == "up" and not model.matched[i]:
            if index >= 0:
                model.state[i] = "down"
                model.state[index] = "down"
                break
            else:
                index = i

    data = {
        "message": "OK"
    }
    return flask.make_response(data,  200)

if __name__ == '__main__':
    app.run(debug=True)
