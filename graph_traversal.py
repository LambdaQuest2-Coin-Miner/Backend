import random
import requests
import time
import json
import socket
from config import API_TOKEN

#api endpoints
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

# init 
INIT_URL = BASE_URL + "init/"

# movement
MOVE_URL = BASE_URL + "move/"

#status / inventory

STATUS_URL = BASE_URL + "status/"

headers = {'Authorization': f'Token {API_TOKEN}'}

from util import Queue, Stack

reverese_directions = {'n':'s', 's':'n','e':'w','w':'e'}

reverse_path = []
visited = {}

# Send request to init to get the current room information
def get_room_info():
    req = requests.get(url = INIT_URL, headers=headers)
    # getting data in the json format
    data = req.json()
    print('data', data)
    return data

# create movement function  
        #set direction/movement via a variable through the object

def move_next_direction(room, visited):

    # maintain tracking information 
    #info = get_room_info()
    # use post request with authorization token 
#     req = requests.post(url = MOVE_URL, headers=headers)
#     data = req.json()
#     print('data post', data)
#     print('data post == ', data[room], data[visited])
#     return data
# move_next_direction([], [])
    # keep track of cooldown
    # keep track of direction being moved
    # room_id is needed when keeping track of directions moved
    # keep track of - title, description, coordinates, players, items, exits, cooldown, messages






#get_room_info()