from datetime import datetime, timedelta
import requests
import time
import re

class Finder:
    def __init__(self):
        self.logs_link = 'https://logs.mcskill.net/?serverid=206&subdir=/Logs/'
        self.global_check = ['[G]']
        self.local_check = ['[L]']
        self.commands_check = ['/']
        self.discipline_commands_check = ['/warn ', '/mute ', '/tempmute ', '/kick ', '/tempban ', '/ban ']
        self.pm_check = ['/m ', '/r ', '/w ', '/msg ']


    def check_logs(self, data_search, data_nicknames, first_date, second_date):
        print('1')
        logs = self.download_logs(first_date, second_date)
        log_list = []
        data_logs_after_all_search = []
        list_string_format = ''
        print('2')

        if data_nicknames: # Поиск по никам
            for z in data_nicknames: # Перебираем каждый ник в переменную z
                for day in logs: # Перебераем каждый день в списке логов
                    after_search = []
                    o = ''
                    for log in day.split('\n'): # Проверяем каждый лог в дне
                        pattern = r'\b{}\b'.format(re.escape(z))
                        if re.search(pattern, log):
                            after_search.append(log)
                    else:
                        for a in after_search: # Преобразуем список в строку
                            o += f'{a}\n'
                        else:
                            log_list.append(o) # Добавляем полученную строку обратно в список дней
        else: # Если нет ников, перекидываем данные из переменной logs в переменную logs_list
            for i in logs:
                log_list.append(i)

        for z in data_search:
            for day in log_list:
                after_search = []
                o = ''
                for log in day.split('\n'):
                    pattern = r'\b{}\b'.format(re.escape(z))
                    if re.search(pattern, log):
                        after_search.append(log)
                else:
                    for a in after_search:
                        o += f'{a}\n'
                    else:
                        data_logs_after_all_search.append(o)
        else:
            print(data_logs_after_all_search)
            for day in data_logs_after_all_search:
                day.sort(key=self.extract_time)
                for z in day:
                    print(list_string_format)
                    list_string_format += f"{z}\n"
                else:
                    list_string_format += '\n\n'
            else:
                print('3')
                return list_string_format


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
