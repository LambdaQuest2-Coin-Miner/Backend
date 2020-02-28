import random
import requests
import time
import json
import socket
from config import API_TOKEN
from player import Player
from cool_down_util import cooldown_calc

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

# Get player status
def get_player_status():
	req = requests.post(url=STATUS_URL, headers=headers)
	data = req.json()
	print('player_data', data)
	return data

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
	#info = get_room_info()
	DIRECTIONS = {'direction': direction}
	# cooldown = info['cooldown']
	# timeout = socket.settimeout()
	# timeout(cooldown)
	#req = requests.post(url = MOVE_URL, json={"exit":"n"}, headers=headers)
	req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	data = req.json()
	print('data post', data)
	
	#     print('data post == ', data[room], data[visited])

	# Calculate cooldown points
	player_status = get_player_status()
	print(f"player cooldown points: {player_status['cooldown']}")

	try:
		cooldown_points = cooldown_calc(player_status['cooldown'], data['cooldown'], data['errors'], data['messages'])
	except KeyError:
		print('No messages')
		cooldown_points = cooldown_calc(player_status['cooldown'], data['cooldown'], data['errors'])

	print('cooldown points: ', cooldown_points)
	return data

#def bfs_next_
	
def find_next_path(visited):
	room_info = get_room_info()
	room_id = room_info['room_id']
	cooldown = room_info['cooldown']
	time.sleep(cooldown)
	queue = Queue()
	traveled_rooms = set()
	# queue.enqueue([room_info[room_id]])
	# stack a list for next path
	queue.enqueue([visited])

	while queue.size() > 0:
		current_path = queue.dequeue()
		# possibly should be room_node = current_path[-1][1] ?
		room_node = current_path[-1]

		time.sleep(cooldown)
		for pair in current_path:
			if pair[0] is not None:
				traversal_path.append(pair[0])
			return traversal_path

		if room_node not in traveled_rooms:
			traveled_rooms.add(room_node)
			exits = visited[room_node]['exits']
			# for exit in exits:
			# 	path_copy = list(current_path)
			# 	path_copy.append(exit, exits[exit])
			# 	queue.enqueue(path_copy)
			# 	print('enqueued', path_copy)
			for exit in exits:
				path_copy = list(current_path)
				if exit == "?":
					print('question marks', exit)
					pass
				else:
					#path_copy = list(current_path)
					path_copy.append(exit, exits[exit])
					queue.enqueue(path_copy)
					print('enqueued')
	return


# find_next_path('e')

move_next_direction('e')

room_graph = get_room_info()


# visited[player.current_room.id] = player.current_room.get_exits()


