import random
import requests
import time
import json
import socket
from config import API_TOKEN
#from player import Player
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

r = requests.get(f"{BASE_URL}/init/", headers=headers).json()

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
	print('data from room info', data)
	return data

# randomizer is here from a Graphs project as an alternative way to traverse the graph
def randomizer(room_id, doors):
	req = requests.get(url = INIT_URL, headers=headers)
	# getting data in the json format
	data = req.json()
	print('data from room info', data)
	
	
	# data = get_room_info()
	if len(doors) > 1:
		
		rando = random.randint(1,len(doors)-1)
		print(f"from randomizer {room_id} {doors[rando]}")
		return doors[rando]
	else:
		doors = data
		print('data in randomizer', doors)
		return doors
	# return data


def find_next_dir(current_room, visited):
    #  picks a random unexplored direction from the player's current room's exits list, 
    # If no available exits, return None

    # get allowed exits from the current_room
    travel_dir = None
    cooldown = 0
    if current_room not in visited:
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
	
	DIRECTIONS = {'direction': direction}
	
	print(f"room room: {r['room_id']}")
	# cooldown = info['cooldown']
	# timeout = socket.settimeout()
	# timeout(cooldown)
	#req = requests.post(url = MOVE_URL, json={"exit":"n"}, headers=headers)
	req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	data = req.json()
	print('data post move next direction', data)
	room_id = r['room_id']
	cooldown = r['cooldown']
	print('room_id', room_id)
	time.sleep(cooldown)
	if room_id in visited and visited[room_id]['directions'][direction] != '?':
		next = visited[room_id]['directions'][direction]
		DIRECTIONS = {'next_room_id': next}
	req = requests.post(url = MOVE_URL, json=DIRECTIONS, headers=headers)
	# Calculate cooldown points
	player_status = get_player_status()
	print(f"player cooldown points: {player_status['cooldown']}")
	try:
		cooldown_points = cooldown_calc(player_status['cooldown'], data['cooldown'], data['errors'], data['messages'])
	except KeyError:
		print('No messages')
		cooldown_points = cooldown_calc(player_status['cooldown'], data['cooldown'], data['errors'])

	print('cooldown points: ', cooldown_points)
	#print('move data room and cool', (data['room_id', data['cooldown']]))
	#return (data['room_id', data['cooldown']])
	return data
	
def find_next_path(visited):
	room = r['room_id']
	cooldown = r['cooldown']
	time.sleep(cooldown)
	queue = Queue()
	traveled_rooms = set()
	# queue.enqueue([(None, room_id)])
	# stack a list for next path
	# queue.enqueue([room])
	queue.enqueue([(None, room)])

	while queue.size() > 0:
		current_path = queue.dequeue()
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
				path_copy.append(exit, exits[exit])
				queue.enqueue(path_copy)
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
	data = get_room_info()
	cooldown = data['cooldown']
	print('rrrrrrr', r)
	# connecting to room_id (having trouble accessing init object (point is to get the room_id but for some reason it does not in some cases))
	room = r['room_id']
	# invoking cooldown 
	time.sleep(cooldown)
	# Point of this is to try to find the next room and cooldown connects to finding the next current room that has not been explored yet. 
	next_room, cooldown = find_next_dir(room, visited)
	# waiting for cooldown here.. 
	time.sleep(cooldown)
	# while the next direction is not None.. 
	while next_room is not None:
		## set the new room and cooldown to match the players next direction with the current room and visited called 
		room_explored, cooldown = move_next_direction(next_room, visited)
		# cooldown.. am I using cool down too much?
		time.sleep(cooldown)

		# semi forgot what I was trying to do here, but the intention is to save the new room in the current room's direction
		visited[room]['directions'][next_room] = room_explored
		# here is to save the current room in the new room's direction
		if room_explored not in visited:
			# room_info = get_room_info()
			# room_info = r()
			# print('room_info', r())
			## this is to print out the information needed from the init function 
			exits = r['exits']
			coordinates = r['coordinates']
			cooldown = r['cooldown']
			title = r['title']
			time.sleep(cooldown)
			directions_to_visit = {}
			for direction in exits:
				if direction == reverese_directions[next_room]:
					directions_to_visit[direction] = room
				else:
					directions_to_visit[direction] = '?'

			room_information = {}
			room_information['directions'] = directions_to_visit
			room_information['coordinates'] = coordinates
			room_information['title'] = title
			visited[room_explored] = room_information
		else:
			visited[room_explored]['directions'][reverese_directions[next_room]] = room

		next_room, cooldown = find_next_dir(room_explored, visited)

		time.sleep(cooldown)

		room = r['room_id']
		cooldown = r['cooldown']
		time.sleep(cooldown)
		

# 	next_path

# find_next_path()


room_graph = get_room_info()

travel_through_map = True

# intention is to continously look through new rooms with while loop until all are visited.. 
while travel_through_map is True:
	# invoking traversal to end paths
	traversal_path_end(visited)
	#randomizer(r['room_id'], visited)
	# print('randomize', randomizer(data['room_id'], visited))

	path_loop = find_next_path(visited)
	if path_loop is not None:
		print('path loop printing: ', path_loop)
		
		# move_next_direction('s')
		# move_next_direction('w')
		for path in path_loop:
			room_explored, cooldown = move_next_direction(path, visited)
			time.sleep(cooldown)
	else:
		travel_through_map = False

# visited[player.current_room.id] = player.current_room.get_exits()
# Final graph - after visiting all rooms
print(f"GRAPH: {visited}")
with open('graph.json', 'w') as fp:
    json.dump(visited, fp)