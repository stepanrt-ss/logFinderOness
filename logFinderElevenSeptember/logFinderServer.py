import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import FinderLogs
import time
import json


app = Flask(__name__)
CORS(app)
list_checker = []
nicks = []
finder = FinderLogs.Finder()


@app.route('/login', methods=['POST'])
def authorization():
    try:
        response = request.json
        name = response.get('login')
        password = response.get('password')
        with open(f'{name}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data['login'] == name and data['password'] == password:
                return jsonify({'message': 'success'}), 200
            else:
                return jsonify({'message': 'wrong pass or login'}), 200
    except:
        return jsonify({'message': 'error'}), 400

@app.route('/writePosPlayer', methods=['POST'])
def write_data():
    response = request.json
    pos_player = response.get('data')
    print(pos_player)
    with open('../AnB/logsPosPlayer.txt', 'a', encoding='utf-8') as f:
        f.write(f"{pos_player}\n")

    return jsonify({'message': 'success'}), 200


@app.route('/getLogs', methods=['POST'])
def send_data():
    global nicks
    data_response = request.json
    data_search = data_response.get('data_search')
    first_date = data_response.get('first_date')
    second_date = data_response.get('second_date')
    data_nicknames = data_response.get('nicknames')
    logs = finder.check_logs(data_search, data_nicknames, first_date, second_date)
    print(logs)
    if logs:
        return jsonify({'logs': logs}), 200
    else:
        return jsonify({'message': 'error'}), 400


    # if not list_checker and not nicks:
    #     return jsonify({'logs': finder.download_logs(first_date=data_response.get('first_date'), second_date=None)}), 200
    # return jsonify({'logs': finder.download_logs(first_date=data_response.get('first_date'), second_date=None)}), 200


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
