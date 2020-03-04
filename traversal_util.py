import requests
import json

# api endpoints
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
# init
INIT_URL = BASE_URL + "init/"
#status / inventory
STATUS_URL = BASE_URL + "status/"

# api headers
f = open("game_token.txt", "r")
GAME_TOKEN = f.read()
# print(f"Game token is {GAME_TOKEN}")
f.close()
HEADERS = {'Authorization': f'Token {GAME_TOKEN}'}

# Get player status


def get_player_status():
    req = requests.post(url=STATUS_URL, headers=HEADERS)
    data = req.json()
    #print('player_data status:', data)
    return data


# Get current room info
def get_room_info():
    req = requests.get(url=INIT_URL, headers=HEADERS)
    # getting data in the json format
    info = req.json()
    #print('data from room info', info)
    return info
