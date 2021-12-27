from flask import Flask, jsonify, request
from settings import settings, update 
import subprocess

app = Flask(__name__)

@app.route('/say', methods=['POST'])
def say():
    to_say = request.data
    if len(to_say) == 0:
        return 'You must say something', 400

    limit = 100
    if len(to_say) > limit:
        return f'You are trying to say too much. The limit is {limit} characters', 400

    subprocess.run(['espeak', request.data])

    return f'You did it. You said {to_say}'

@app.route('/', methods=['GET'])
def get():
    return jsonify(settings().to_dict())

@app.route('/', methods=['POST'])
def post():
    try:
        if request.json is None:
            raise TypeError('request body must not be None')

        update(**request.json)
        return jsonify(settings().to_dict())
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
