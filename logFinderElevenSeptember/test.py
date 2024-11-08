import json

json_data = {'login':'verno', 'password':'sadahuwhduhasd2', 'auth_token':'sdayhhcauyuteaf82313fdba27'}


# with open('verno.json', 'w', encoding='utf-8') as f:
#     json.dump(json_data, f, indent=4)


with open('verno.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    login = data['login']
    password = data['password']
    auth_token = data['auth_token']
    print(login)
    print(password)
    print(auth_token)