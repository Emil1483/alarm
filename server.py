from flask import Flask, jsonify, request
from settings import settings, update 

app = Flask(__name__)

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
