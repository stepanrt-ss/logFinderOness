from datetime import datetime, timedelta
import requests
import time
import re



class Finder:
    def __init__(self):
        self.logs_link = 'https://logs.mcskill.net/?serverid=206&subdir=/Logs/'


    def search_func(self, data_search, logs):
        after_list = []
        print(data_search)
        for element in data_search:
            print(element)
            for day in logs:
                for log in day.split('\n'):
                    pattern = r'{}'.format(re.escape(element))
                    if re.search(pattern, log):
                        after_list.append(log)
        else:
            after_list.sort(key=self.extract_time)
            return after_list


    @staticmethod
    def extract_time(log_entry):
        if len(log_entry) < 4:
            pass
        else:
            time_str = log_entry.split(' ')[1].replace(']', '')
            return datetime.strptime(time_str, "%H:%M:%S")


    def download_logs(self, first_date, second_date):
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
                response = requests.get(url=f"{self.logs_link}{date_search}.txt")
                logs.append(response.text)
                time.sleep(0.5)
            else:
                return logs
        else:
            day = first_date.split('-')[2]
            month = first_date.split('-')[1]
            year = first_date.split('-')[0]
            date_search = f'{day}-{month}-{year}'
            response = requests.get(url=f"{self.logs_link}{date_search}.txt")
            logs.append(response.text)
            return logs
