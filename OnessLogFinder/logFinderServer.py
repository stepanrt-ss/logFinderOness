import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import FinderLogs
import time
import json
import os


app = Flask(__name__)
CORS(app)
list_checker = []
nicks = []
finder = FinderLogs.Finder()


@app.route('/login', methods=['POST'])
def authorization():
    try:
        response = request.json
        token = response.get('auth_token')
        name = response.get('login')
        password = response.get('password')
        users_list = os.listdir('/users')
        for i in users_list:
            with open(f'{i}.json', 'r', encoding='utf-8') as f:
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
    server_id = data_response.get('server_id')

    # сервер не хавает .split Из-за сатрой версии python на нем
    try:
        data_nicknames = data_response.get('nicknames').split(',')
    except:
        data_nicknames = False

    download_logs = finder.download_logs(first_date, second_date, server_id)
    list_logs = finder.search_func(data_search, download_logs)
    string_format = ''

    if data_nicknames:
        logs_with_check_nicks = finder.search_func(data_nicknames, list_logs)
        for i in logs_with_check_nicks:
            string_format += f'{i}\n'
        return jsonify({'logs': string_format}), 200
    else:
        for i in list_logs:
            string_format += f'{i}\n'
        return jsonify({'logs': string_format}), 200


    # if not list_checker and not nicks:
    #     return jsonify({'logs': finder.download_logs(first_date=data_response.get('first_date'), second_date=None)}), 200
    # return jsonify({'logs': finder.download_logs(first_date=data_response.get('first_date'), second_date=None)}), 200


if __name__ == '__main__':
    app.run(debug=True, host='194.87.43.6', port='8041')
