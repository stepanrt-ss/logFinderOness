
from flask import Flask, request, jsonify
from flask_cors import CORS
import FinderLogs
from OnessLogFinder.test import nickname

app = Flask(__name__)
CORS(app)
list_checker = []
nicks = []
finder = FinderLogs.Finder()

@app.route('/getNicks', methods=['POST'])
def send_nicks():
    to_json = {'HTC Titan': finder.get_list_players('HTC Titan'), 'HTC Phobos': finder.get_list_players('HTC Phobos'), 'HTC Elara': finder.get_list_players('HTC Elara')}



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


if __name__ == '__main__':
    app.run(debug=True, host='194.87.43.6', port='8041')
