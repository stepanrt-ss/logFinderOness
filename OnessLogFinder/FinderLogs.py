from datetime import datetime, timedelta
import requests
import time
import re


class Finder:
    def __init__(self):
        self.logs_titan = 'https://logs.mcskill.net/index.php?serverid=50&subdir=/Logs/'
        self.logs_phobos = 'https://logs.mcskill.net/index.php?serverid=203&subdir=/Logs'
        self.logs_elara = 'https://logs.mcskill.net/index.php?serverid=206&subdir=/Logs/'


    def search_func(self, data_search, logs):
        after_list = []
        for element in data_search:
            for day in logs:
                for log in day.split('\n'):
                    pattern = r'{}'.format(re.escape(element))
                    if re.search(pattern, log):
                        after_list.append(log)
        else:
            after_list.sort(key=self.extract_datetime)
            return after_list


    @staticmethod
    def extract_datetime(log_entry):
        """
        Извлекает полную дату и время из строки лога.
        Предполагается, что формат строки: [DD.MM.YYYY HH:MM:SS] ...
        """
        try:
            date_time_str = log_entry.split(']')[0].replace('[', '')  # [13.11.2024 00:18:46] -> 13.11.2024 00:18:46
            return datetime.strptime(date_time_str, "%d.%m.%Y %H:%M:%S")
        except (ValueError, IndexError):
            return datetime.min  # Если не удаётся разобрать, вернуть минимальное значение


    def download_logs(self, first_date, second_date, server_id):
        response = None
        intermediate_dates = []
        logs = []
        if second_date:
            start_date = datetime.strptime(first_date, '%Y-%m-%d')
            end_date = datetime.strptime(second_date, '%Y-%m-%d')
            current_date = start_date
            while current_date <= end_date:
                intermediate_dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

            for i in intermediate_dates:
                day = i.split('-')[2]
                month = i.split('-')[1]
                year = i.split('-')[0]
                date_search = f'{day}-{month}-{year}'
                if server_id == 'HTC Titan':
                    response = requests.get(url=f"{self.logs_titan}{date_search}.txt")
                elif server_id == 'HTC Phobos':
                    response = requests.get(url=f"{self.logs_phobos}{date_search}.txt")
                elif server_id == 'HTC Elara':
                    response = requests.get(url=f"{self.logs_elara}{date_search}.txt")
                logs.append(response.text)
                time.sleep(0.5)
            else:
                return logs
        else:
            day = first_date.split('-')[2]
            month = first_date.split('-')[1]
            year = first_date.split('-')[0]
            date_search = f'{day}-{month}-{year}'
            response = requests.get(url=f"{self.logs_elara}{date_search}.txt")
            logs.append(response.text)
            return logs


    def get_list_players(self, server_id):
        pass
