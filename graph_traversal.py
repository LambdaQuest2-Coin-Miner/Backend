import random
import requests
import time
import json
import socket
from config import API_TOKEN
#from player import Player
from cool_down_util import cooldown_calc
from util import Queue, Stack

# api endpoints
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

# init
INIT_URL = BASE_URL + "init/"

# movement
MOVE_URL = BASE_URL + "move/"

#status / inventory

STATUS_URL = BASE_URL + "status/"

headers = {'Authorization': f'Token {API_TOKEN}'}


r = requests.get(f"{BASE_URL}/init/", headers=headers).json()

reverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

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

def find_next_dir(current_room, visited, player_status):
	print(f"RECEIVED CURRENT_ROOM: {current_room}")
	# Picks a random unexplored direction from available rooms exit list; returns None if no exits avail

	# get allowed exits from the current_room
	travel_dir = None
	try:
		cooldown = cooldown_calc(
			player_status['cooldown'], current_room['cooldown'], current_room['errors'], current_room['messages'])
	except KeyError:
		print("No messages")
		cooldown = cooldown_calc(
			player_status['cooldown'], current_room['cooldown'], current_room['errors'])

	if current_room['room_id'] not in visited:
		# Wait for cooldown
		time.sleep(cooldown)
		directions = {}
		for direction in current_room['exits']:
			directions[direction] = '?'
		current_room['directions'] = directions
		visited[current_room['room_id']] = current_room
		print(f"NEWLY VISITED STATUS: {visited}")
		travel_dir = random.choice(list(directions.keys()))
	else:
		# check if there's an exit that is not ?
		directions = visited[current_room['room_id']]['directions']
		print(f"ALREADY VISITED STATUS: {visited}")
		print(f"DIRECTIONS: {directions}")
		possible_dirs = []
		for direction in directions:
			if directions[direction] == '?':
				possible_dirs.append(direction)
		if len(possible_dirs) != 0:
			travel_dir = random.choice(possible_dirs)
			print(f"TRAVEL_DIR: {travel_dir} COOLDOWN: {cooldown}")
	return (travel_dir, cooldown)


# create movement function
	# set direction/movement via a variable through the object
def move_next_direction(direction, current_room, visited, player_status):
	# if current_room['room_id'] in visited and visited[current_room['room_id']]['directions'][direction] != '?':
	#if direction in current_room['exits']:
	print(f"DIRECTION ATTEMPT: {direction}")
	req = requests.post(url=MOVE_URL, json={
						"direction": direction}, headers=headers)
	room = req.json()
	print(f"NEXT ROOM INFO: {room}")

	# else:
	# 	room = current_room
	# 	print(f"USING ROOM INFO: {room}")

	# Calculate cooldown points
	try:
		cooldown = cooldown_calc(
			player_status['cooldown'], room['cooldown'], room['errors'], room['messages'])
	except KeyError:
		print('No messages')
		cooldown = cooldown_calc(
			player_status['cooldown'], room['cooldown'], room['errors'])

	return (room, cooldown)

	# else:
	# 	print(f"EXIT NOT AVAILABLE")
	# 	return (None, 0)


def find_next_path(visited, player_status):
	room = get_room_info()
	#room = data['room_id']
	#cooldown = data['cooldown']
	# room = r['room_id']
	# cooldown = r['cooldown']
	#time.sleep(cooldown)
	q = Queue()
	traveled_rooms = set()
	# queue.enqueue([(None, room_id)])
	# stack a list for next path
	# queue.enqueue([room])
	q.enqueue([(None, room)])

	while q.size() > 0:
		current_path = q.dequeue()
		# possibly should be room = current_path[-1][1] ?
		current_room = current_path[-1][1]
		print(f"CURRENT PATH: {current_path} CURRENT ROOM: {current_room}")
		direction, cooldown = find_next_dir(current_room, visited, player_status)
		time.sleep(cooldown)
		if direction is not None:
			path = []
			for pair in current_path:
				if pair[0] is not None:
					path.append(pair[0])
			return path

		if current_room['room_id'] not in traveled_rooms:
			traveled_rooms.add(current_room['room_id'])
			exits = visited[current_room['room_id']]['directions']
			print(f"FIND_NEXT_PATH EXITS: {exits}")
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


def traversal_path_end(visited, player_status):
	room = get_room_info()
	print('ROOM INFO:', room)

	next_direction, cooldown = find_next_dir(room, visited, player_status)
	# waiting for cooldown here..
	time.sleep(cooldown)
	# while the next direction is not None..
	while next_direction is not None:
		# set the new room and cooldown to match the players next direction with the current room and visited called
		if next_direction in room['exits']:
			print(f"LET'S EXPLORE heading {next_direction}")
			room_explored, cooldown = move_next_direction(next_direction, room, visited, player_status)
			time.sleep(cooldown)

			# here is to save the current room in the new room's direction
			if room_explored['room_id'] not in visited:
				directions_to_visit = {}
				
				for direction in room_explored['exits']:
					if direction == reverse_directions[next_direction]:
						directions_to_visit[direction] = room['room_id']
					else:
						directions_to_visit[direction] = '?'

				room_explored['directions'] = directions_to_visit
				visited[room_explored['room_id']] = room_explored
			else:
				visited[room_explored['room_id']
					]['directions'][reverse_directions[next_direction]] = room['room_id']
				next_direction, cooldown = find_next_dir(
						room_explored, visited, player_status)

				time.sleep(cooldown)
				room = get_room_info()





# 	next_path

# find_next_path()

# room_graph = get_room_info()

travel_through_map = True
PLAYER_STATUS = get_player_status()
# intention is to continously look through new rooms with while loop until all are visited..
while travel_through_map is True:
	print('visited: ', visited)
	# invoking traversal to end paths
	traversal_path_end(visited, PLAYER_STATUS)
	#randomizer(r['room_id'], visited)
	# print('randomize', randomizer(data['room_id'], visited))

	try:
		path_loop = find_next_path(visited, PLAYER_STATUS)

		if path_loop is not None:
			print('path loop printing: ', path_loop)
			for path in path_loop:
				print(f"PATH IS {path}")
				#time.sleep(cooldown)
		else:
			travel_through_map = False
	except:
		print(f"BFS attempt failed number of rooms visited: {len(visited)}")

# visited[player.current_room.id] = player.current_room.get_exits()
# Final graph - after visiting all rooms
print(f"GRAPH: {visited}")
with open('graph.json', 'w') as fp:
    json.dump(visited, fp)
