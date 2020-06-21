import requests
import json
import telebot
from time import sleep

url_bot = "<token>"

def auth_git():
    r = requests.get('https://api.github.com/user', headers={'Authorization': 'token <token>'})
    data = r.json()
    count_rep = data['public_repos']
    return count_rep
    
def check_update_git(count_rep):
    r = requests.get('https://api.github.com/user', headers={'Authorization': 'token <token>'})
    data = r.json()
    tmp_new = data['public_repos']
    if (count_rep < tmp_new):
        count_rep = tmp_new
        return True
    else:
        return False
        
def get_updates_json(request):  
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()
    
def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]
    
def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url_bot + 'sendMessage', data=params)
    return response



if __name__ == '__main__': 
    update_id = last_update(get_updates_json(url_bot))['update_id']
    count_rep = auth_git()
    while True:
        if update_id == last_update(get_updates_json(url_bot))['update_id']:
           if (check_update_git(count_rep)):
            send_mess(get_chat_id(last_update(get_updates_json(url_bot))), 'Количесто репозиториев изменилось, стало:' + str(count_rep))
           else:
            send_mess(get_chat_id(last_update(get_updates_json(url_bot))), 'Количесто репозиториев осталось прежним:' + str(count_rep))
           update_id += 1
        sleep(1) 

    
