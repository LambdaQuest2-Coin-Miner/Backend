import random
import requests
import time
import json
import socket
from config import API_TOKEN
#from player import Player
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


r = requests.get(f"{BASE_URL}/init/", headers=headers).json()

reverse_directions = {'n':'s','s':'n','e':'w','w':'e'}

reverse_path = []
visited = {}
traversal_path = []

# Get player status
def get_player_status():
	req = requests.post(url=STATUS_URL, headers=headers)
	data = req.json()
	print('player_data status:', data)
	return data


# Send request to init to get the current room information
def get_room_info():
	req = requests.get(url=INIT_URL, headers=headers)
	# getting data in the json format
	data = req.json()
	print('data from room info', data)
	return data

# randomizer is here from a Graphs project as an alternative way to traverse the graph
# def randomizer(room_id, doors):
# 	req = requests.get(url = INIT_URL, headers=headers)
# 	# getting data in the json format
# 	data = req.json()
# 	print('data from room info', data)
	
	
# 	# data = get_room_info()
# 	if len(doors) > 1:
		
# 		rando = random.randint(1,len(doors)-1)
# 		print(f"from randomizer {room_id} {doors[rando]}")
# 		return doors[rando]
# 	else:
# 		doors = data
# 		print('data in randomizer', doors)
# 		return doors
# 	# return data


def find_next_dir(current_room, visited):
	# Picks a random unexplored direction from available rooms exit list; returns None if no exits avail

	# get allowed exits from the current_room
	travel_dir = None
	cooldown = 0
	if current_room not in visited:
		r = get_room_info()
		exits = r['exits']
		coordinates = r['coordinates']

		cooldown = r['cooldown']
		title = r['title']
		# Wait for cooldown
		time.sleep(cooldown)
		directions = {}
		for direction in exits:
			directions[direction] = '?'
		info = {}
		info['directions'] = directions
		info["coordinates"] = coordinates
		info['title'] = title
		visited[current_room] = info
		travel_dir = random.choice(list(directions.keys()))
	else:
		# check if there's an exit that is not ?
		directions = visited[current_room]['directions']
		possible_dirs = []
		for direction in directions:
			if directions[direction] == '?':
				possible_dirs.append(direction)
		if len(possible_dirs) != 0:
			travel_dir = random.choice(possible_dirs)
	return (travel_dir, cooldown)

# create movement function  
		#set direction/movement via a variable through the object

def move_next_direction(direction, visited):
	# maintain tracking information 
	# use post request with authorization token 
	
	DIRECTIONS = {"direction": direction}
	
	data = get_room_info()
	room = data['room_id']
	
	# cooldown = data['cooldown']
	# # timeout = socket.settimeout()
	# # timeout(cooldown)
	# time.sleep(cooldown)
	#req = requests.post(url = MOVE_URL, json={"exit":"n"}, headers=headers)
	#req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	# info = req.json()
	if room in visited and visited[room]['directions'][direction] != '?':
		next = visited[room]['directions'][direction]
		DIRECTIONS['next_room_id'] = f"{next}"
		#DIRECTIONS = {'next_room_id': next}
	req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	#print('data info post move next direction', data)
	# Calculate cooldown points
	data = req.json()
	player_status = get_player_status()
	#print(f"room room: {r['room_id']}")
	print(f"player cooldown points: {player_status['cooldown']}")
	try:
		cooldown_points = cooldown_calc(player_status['cooldown'], data['cooldown'], data['errors'], data['messages'])
	except KeyError:
		print('No messages')
		cooldown_points = cooldown_calc(player_status['cooldown'], data['cooldown'], data['errors'])

	print('cooldown points: ', cooldown_points)
	print('move data room and cool', (data['room_id'], data['cooldown']))
	return (data['room_id'], data['cooldown'])
	# return data


	
def find_next_path(visited):
	data = get_room_info()
	room = data['room_id']
	cooldown = data['cooldown']
	# room = r['room_id']
	# # cooldown = r['cooldown']
	time.sleep(cooldown)
	q = Queue()
	traveled_rooms = set()
	# queue.enqueue([(None, room_id)])
	# stack a list for next path
	# queue.enqueue([room])
	q.enqueue([(None, room)])

	while q.size() > 0:
		current_path = q.dequeue()
		# possibly should be room_node = current_path[-1][1] ?
		room_node = current_path[-1][1]
		direction, cooldown = find_next_dir(room_node, visited)
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
			for exit in exits:
				path_copy = list(current_path)
				path_copy.append((exit, exits[exit]))
				q.enqueue(path_copy)
				print('enqueued', path_copy)
			
			# for exit in exits[exit]["exits"].key():
			# 	new_direction = exits[exit]["exits"][exit]
			# 	path_copy = list(current_path)
			# 	if exit == "?":
			# 		print('question marks', exit)
			# 		pass
			# 	else:
			# 		#path_copy = list(current_path)
			# 		path_copy.append(new_direction)
			# 		#path_copy.append(exit, exits[exit])
			# 		queue.enqueue(path_copy)
			# 		print('enqueued')
	return None

def traversal_path_end(visited):
	# r = requests.get(f"{BASE_URL}/init/", headers=headers).json()
	# print(r)
	# print(f"Starting room: {r['cooldown']}")
	data = get_room_info()
	print('data info traversal', data)
	room = r['room_id']
	print('room in traversal', room)
	cooldown = data['cooldown']
	time.sleep(cooldown)
	# connecting to room_id (having trouble accessing init object point is to get the room_id but for some reason it does not in some cases))
	# Point of this is to try to find the next room and cooldown connects to finding the next current room that has not been explored yet. 
	next_room, cooldown = find_next_dir(room, visited)
	# waiting for cooldown here.. 
	time.sleep(cooldown)
	# while the next direction is not None.. 
	while next_room is not None:
		## set the new room and cooldown to match the players next direction with the current room and visited called 
		
		room_explored, cooldown = move_next_direction(next_room, visited)
		#print('room_explored ', room_explored)
		#print('and cooldown', cooldown)
		# cooldown.. am I using cool down too much?
		time.sleep(cooldown)

		# semi forgot what I was trying to do here, but the intention is to save the new room in the current room's direction
		visited[room]['directions'][next_room] = room_explored
		# here is to save the current room in the new room's direction
		if room_explored not in visited:
			data = get_room_info()
			#print('data in room_explored not in visited', data)
			
			# room_info = get_room_info()
			# room_info = r()
			# print('room_info', r())
			## this is to print out the information needed from the init function 
			# exits = data['exits']
			# coordinates = data['coordinates']
			# title = data['title']
			exits = r['exits']
			coordinates = r['coordinates']
			title = r['title']
			cooldown = data['cooldown']
			
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

		next_room, cooldown = find_next_dir(room_explored, visited)
		time.sleep(cooldown)
		data = get_room_info()

		room = r['room_id']
		cooldown = data['cooldown']
		time.sleep(cooldown)
		

# 	next_path

# find_next_path()

# room_graph = get_room_info()

travel_through_map = True

# intention is to continously look through new rooms with while loop until all are visited.. 
while travel_through_map is True:
	print('visited: ', visited)
	# invoking traversal to end paths
	traversal_path_end(visited)
	#randomizer(r['room_id'], visited)
	# print('randomize', randomizer(data['room_id'], visited))

	path_loop = find_next_path(visited)
	if path_loop is not None:
		print('path loop printing: ', path_loop)
		for path in path_loop:
			room_explored, cooldown = move_next_direction(path, visited)
			#time.sleep(cooldown)
	else:
		travel_through_map = False

# visited[player.current_room.id] = player.current_room.get_exits()
# Final graph - after visiting all rooms
print(f"GRAPH: {visited}")
with open('graph.json', 'w') as fp:
	json.dump(visited, fp)