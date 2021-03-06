import subprocess
from threading import Thread

from flask import Flask, jsonify, request

import alarm
from settings import settings, update

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

@app.route('/test', method=['POST'])
def test():
    try:
        f = lambda : alarm.main(test=True)
        Thread(target=f).start()
        return 'Started alarm test'
    except Exception as e:
        return str(e), 500

@app.route('/start', method=['POST'])
def start():
    try:
        Thread(target=alarm.main).start()
        return 'Started alarm'
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
