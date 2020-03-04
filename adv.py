# import time
# #import requests
# from util import Queue, Stack
# # from room import Room
# from player import Player
# # from world import World

# import random
# from ast import literal_eval








# # player = Player(world.starting_room)
# #sanity check length of room list in txt file
# # print(f"room_graph length: {len(room_graph)}" )


# # Fill this out with directions to walk
# # traversal_path = ['n', 'n']
# traversal_path = []


# graph = {}
# visited = set()
# visitcount = 0

# def backup(last_dir):
#     backtrack = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
#     return backtrack[last_dir]

# def randomizer(room_id, doors):
#     if len(doors) > 1:
#         rando = random. randint(1,len(doors)-1)
#         print(f"from randomizer {room_id} {doors[rando]}")
#         return doors[rando]
#     else:
#         return doors[0]

# src = None
# prev_room = None

# while len(visited) < len(room_graph):
#     print()
#     print(f"round {visitcount} ", end='==============')
#     print()
#     current_room = player.current_room.id
#     # print(current_room)
#     visited.add(current_room)

#     if current_room not in graph:
#         graph[current_room] = {}

#         for exit in player.current_room.get_exits():
#             graph[current_room][exit] = '?'
    
#     availrooms = [key for key,val in graph[current_room].items() if val == '?']

#     if len(availrooms) > 0:
#         visitcount += 1
#         print(f"where am I?: {current_room}")
#         print(f"and where have i been? : {visited}") 
#         print(f"what is already in graph? : {graph}")
#         direction = randomizer(player.current_room.id, availrooms)
#         player.travel(direction)
#         graph[current_room][direction] = player.current_room.id
#         go_back = backup(direction)
#         old_room = current_room
#         traversal_path.append(direction)
    
#     else:
#         def backtrack(graph,player):
#             q = Queue()
#             exploredrooms = set()

#             q.enqueue([(player.current_room.id, None)])

#             while q.size() > 0 :
#                 curr_path = q.dequeue()
#                 lastroom = curr_path[-1][0]

#                 if '?' in graph[lastroom].values():
#                     path = []
#                     for p in curr_path:
#                         path.append(p[1])
#                     print(f"p {p}")
#                     return path

#                 if lastroom not in exploredrooms:
#                     exploredrooms.add(lastroom)

#                     for k,v in graph[lastroom].items():
#                         path_copy = list(curr_path)
#                         path_copy.append((v,k))
#                         q.enqueue(path_copy)
#         retrace_steps = backtrack(graph, player)

#         for steps in retrace_steps:
#             player.travel(steps)
#             traversal_path.append(steps)