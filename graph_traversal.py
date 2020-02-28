import random
import requests
import time
import json
import socket
from config import API_TOKEN
from world import World
from player import Player

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
traversal_path = []

# Send request to init to get the current room information
def get_room_info():
	req = requests.get(url = INIT_URL, headers=headers)
	# getting data in the json format
	data = req.json()
	print('data', data)
	return data

# create movement function  
		#set direction/movement via a variable through the object

def move_next_direction(direction):
	# maintain tracking information 
	# use post request with authorization token 
	info = get_room_info()
	DIRECTIONS = {"direction": direction}

	# cooldown = info['cooldown']
	# timeout = socket.settimeout()
	# timeout(cooldown)
	#req = requests.post(url = MOVE_URL, json={"direction":"n"}, headers=headers)
	req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	data = req.json()
	print('data post', data)
#     print('data post == ', data[room], data[visited])
	print('data cooldown: ', data['cooldown'])
	return data
	


<<<<<<< HEAD
move_next_direction('s')
=======
move_next_direction('e')
>>>>>>> edaeac068523045e603f617837ab4d8d7f2ebc81

room_graph = get_room_info()

# world = World()

# world.load_graph(room_graph)

# player = Player(world.starting_room)

# visited[player.current_room.id] = player.current_room.get_exits()
# player = Player(world.starting_room)


# visited[player.current_room.id] = player.current_room.get_exits()


