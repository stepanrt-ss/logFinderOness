import datetime

import re
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
list_checker = []
nicks = []


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

    if data_response.get('check_global'):
        list_checker.append('[G]')

    if data_response.get('check_local'):
        list_checker.append('[L]')

    if data_response.get('check_commands'):
        list_checker.append('/')

    if data_response.get('check_discipline_commands'):
        list_checker.append('/warn ')
        list_checker.append('/mute ')
        list_checker.append('/tempmute ')
        list_checker.append('/kick ')
        list_checker.append('/tempban ')
        list_checker.append('/ban ')

    if data_response.get('check_pm'):
        list_checker.append('/m ')
        list_checker.append('/r ')
        list_checker.append('/w ')
        list_checker.append('/msg ')

    if data_response.get('nicknames') != '':
        nicks = data_response.get('nicknames').split(',')

    if not list_checker and not nicks:
        return jsonify({'logs': downloadLogs(date=data_response.get('first_date'))}), 200
    return jsonify({'logs': check_logs(data_response.get('first_date'))}), 200


def extract_time(log_entry):
    print(log_entry)
    if len(log_entry) < 4:
        pass
    else:
        time_str = log_entry.split(' ')[1].replace(']', '')
        return datetime.datetime.strptime(time_str, "%H:%M:%S")


def check_logs(data):
    print(nicks)
    global list_checker
    logs = downloadLogs(data)

    v = []
    o = ''

    data_logs = logs.split('\n')
    for x in list_checker:
        for i in data_logs:
            pattern = r'{}'.format(re.escape(x))
            if re.search(pattern, i):
                v.append(i)
    else:
        v.sort(key=extract_time)
        for z in v:
            o += f"{z}\n"
        else:
            list_checker = []
            if nicks:
                return check_nicks(o)
            else:
                return o


def check_nicks(data_logs):
    global nicks
    list_m = []
    o = ''
    print(nicks)
    for z in nicks:
        print('check')
        for i in data_logs.split('\n'):
            pattern = r'\b{}\b'.format(re.escape(z))
            if re.search(pattern, i):
                list_m.append(i)
    else:
        list_m.sort(key=extract_time)
        nicks = []
        for c in list_m:
            o += f"{c}\n"

        return o


def downloadLogs(date):
    day = date.split('-')[2]
    month = date.split('-')[1]
    year = date.split('-')[0]
    date_search = f'{day}-{month}-{year}'
    response = requests.get(url=f"https://logs.mcskill.net/?serverid=206&subdir=/Logs/{date_search}.txt")
    return response.text


if __name__ == '__main__':
    app.run(debug=True, host='194.87.43.6', port=8041)