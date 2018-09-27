
from flask import Flask, abort, request 
import json
from check import SpellCheck

app = Flask(__name__)
spell = SpellCheck()

@app.route('/check', methods=['POST']) 
def check():
    if not request.json:
        abort(400)

    res = spell.check(request.json['mgs'])
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

