import requests
import sys
import json

from time import time, sleep
from traversal_util import get_player_status, get_room_info
from cool_down_util import cooldown_calc

# Load Game Token
f = open("game_token.txt", "r")
GAME_TOKEN = f.read()
print(f"Game token is {GAME_TOKEN}")
f.close()
HEADERS = {'Authorization': f'Token {GAME_TOKEN}'}
MOVE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
PLAYER_STATUS = get_player_status()

def automove(directions):
	current_room = get_room_info()
	print(f"Starting in room:\n {current_room}")
	for direction in directions:
		# Calculate cooldown period
		cooldown = cooldown_calc(
			PLAYER_STATUS['cooldown'], current_room['cooldown'], current_room['errors'], current_room['messages'])
		sleep(cooldown)
		post_data = {"direction": direction[0], "next_room_id": direction[1]}

		# Move player
		try:
			move_player = requests.post(
				url=f"{MOVE_URL}", headers=HEADERS, json=post_data)
			current_room = move_player.json()
			print(f"Move successfully into room:\n {current_room['room_id']}")
		except:
			print(f"An error occurred moving to a room: {move_player['errors']}")
			cooldown = cooldown_calc(
								PLAYER_STATUS['cooldown'], current_room['cooldown'], current_room['errors'])
			# Timeout
			sleep(cooldown)
			cooldown = cooldown_calc(
                            PLAYER_STATUS['cooldown'], current_room['cooldown'], current_room['errors'], current_room['messages'])
			sleep(cooldown)
			move_player = requests.post(
                            url=f"{MOVE_URL}", headers=HEADERS, json=post_data)
			current_room = move_player.json()
			print(f"Move successfully into room:\n {current_room['room_id']}")

	print(f"Auto move complete current room:\n {current_room}")

path = [("n", "117"),("n","108"),("n","78"),("n","22"),("n","18"),("n","12"),("n","9"),("n","3")]

automove(path)
