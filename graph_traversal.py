import random
import requests
import time
import json
from config import API_TOKEN
from cool_down_util import cooldown_calc
from util import Queue, Stack

#api endpoints
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

# init 
INIT_URL = BASE_URL + "init/"

# movement
MOVE_URL = BASE_URL + "move/"

#status / inventory

STATUS_URL = BASE_URL + "status/"

headers = {'Authorization': f'Token {API_TOKEN}'}

reverse_directions = {'n':'s','s':'n','e':'w','w':'e'}

reverse_path = []
traversal_path = []

# Get player status
def get_player_status():
	req = requests.post(url=STATUS_URL, headers=headers)
	data = req.json()
	return data


# Send request to init to get the current room information
def get_room_info():
	req = requests.get(url=INIT_URL, headers=headers)
	# getting data in the json format
	info = req.json()
	#print('data from room info', info)
	return info


def next_dir(room, visited):
	# Picks a random unexplored direction from available rooms exit list; returns None if no exits avail
	travel_dir = None
	cooldown = 0
	if room not in visited:
		info = get_room_info()
		exits = info['exits']
		coordinates = info['coordinates']
		cooldown = info['cooldown']
		title = info['title']
		# cooldown time!
		time.sleep(cooldown)
		directions = {}
		for direction in exits:
			directions[direction] = '?'
		info = {}
		info['directions'] = directions
		info["coordinates"] = coordinates
		info['title'] = title
		visited[room] = info
		travel_dir = random.choice(list(directions.keys()))
	else:
		# checks if an exit is not marked a "?"
		directions = visited[room]['directions']
		possible_dirs = []
		for direction in directions:
			if directions[direction] == '?':
				possible_dirs.append(direction)
		if len(possible_dirs) != 0:
			travel_dir = random.choice(possible_dirs)
	return (travel_dir, cooldown)

def move_next_direction(direction, visited):
	# maintain tracking information 
	# use post request with authorization token 
	
	DIRECTIONS = {"direction": direction}
	
	info = get_room_info()
	room = info['room_id']
	cooldown = info['cooldown']
	time.sleep(cooldown)
	if room in visited and visited[room]['directions'][direction] != '?':
		next = visited[room]['directions'][direction]
		DIRECTIONS["next_room_id"] = f"{next}"
		#DIRECTIONS = {'next_room_id': next}
	req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	data = req.json()
	print('move function room_id and cooldown: ', (data['room_id'], data['cooldown']))
	return (data['room_id'], data['cooldown'])
	# return data


	
def find_next_path(visited):
	info = get_room_info()
	room = info['room_id']
	cooldown = info['cooldown']
	time.sleep(cooldown)
	q = Queue()
	traveled_rooms = set()
	q.enqueue([(None, room)])

	while q.size() > 0:
		current_path = q.dequeue()
		room_node = current_path[-1][1]
		direction, cooldown = next_dir(room_node, visited)
		time.sleep(cooldown)
		if direction is not None:
			path = []
			for pair in current_path:
				if pair[0] is not None:
					path.append(pair[0])
			return path

		if room_node not in traveled_rooms:
			traveled_rooms.add(room_node)
			exits = visited[room_node]['directions']
			for e in exits:
				path_copy = list(current_path)
				path_copy.append((e, exits[e]))
				q.enqueue(path_copy)

	return None

def traversal_path_end(visited):
	info = get_room_info()
	room = info['room_id']
	cooldown = info['cooldown']
	time.sleep(cooldown)
	next_room, cooldown = next_dir(room, visited)
	time.sleep(cooldown)
	# while the next direction is not None
	while next_room is not None:
		# set the new room and cooldown to match the players next direction with the current room and visited called 
		room_explored, cooldown = move_next_direction(next_room, visited)
		# cooldown
		time.sleep(cooldown)
		visited[room]['directions'][next_room] = room_explored
		#save the current room in the new room's direction
		if room_explored not in visited:
			info = get_room_info()
			exits = info['exits']
			coordinates = info['coordinates']
			title = info['title']
			cooldown = info['cooldown']
			time.sleep(cooldown)
			directions_to_visit = {}
			for direction in exits:
				if direction == reverse_directions[next_room]:
					directions_to_visit[direction] = room
				else:
					directions_to_visit[direction] = '?'

			room_information = {}
			room_information['directions'] = directions_to_visit
			room_information['coordinates'] = coordinates
			room_information['title'] = title
			visited[room_explored] = room_information
		else:
			visited[room_explored]['directions'][reverse_directions[next_room]] = room

		next_room, cooldown = next_dir(room_explored, visited)
		time.sleep(cooldown)
		data = get_room_info()
		room = data['room_id']
		cooldown = data['cooldown']
		time.sleep(cooldown)
		

visited = {}
travel_through_map = True

#Continously look through new rooms with while loop until all are visited. 
while travel_through_map is True:
	print('visited: ', visited)
	# invoking traversal to end paths
	traversal_path_end(visited)
	path_loop = find_next_path(visited)
	if path_loop is not None:
		print('path loop printing: ', path_loop)
		for path in path_loop:
			room_explored, cooldown = move_next_direction(path, visited)
			time.sleep(cooldown)
	else:
		travel_through_map = False

# Prints Graph after traversal
print(f"Graph: {visited}")
with open('graph.json', 'w') as fp:
	json.dump(visited, fp)