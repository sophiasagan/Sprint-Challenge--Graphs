from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions = {'n': 's', 'e':'w', 's': 'n', 'w': 'e'} to walk
# traversal_path = ['n', 'n']
traversal_path = []
explored = {}
reverse_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


def bfs(explore):  # returns a path to the closest unexplored path
    q = Queue()
    q.enqueue([player.current_room.id])
    visited = set()

    while q.size() > 0:
        path = q.dequeue()
        cur_room = path[-1]

        if cur_room not in visited:
            visited.add(cur_room)
            # checks for unexplored path
            for direction in explored[cur_room]:
                # return path to an unexplored room
                if explored[cur_room][direction] == '?':
                    return path
                elif explored[cur_room][direction] not in visited:
                    new_path = list(path)
                    new_path.append(explored[cur_room][direction])
                    q.enqueue(new_path)
    return path

def route(room):  # start route
    explored[room.id] = {}
    for next_room in room.get_exits():
        explored[room.id][next_room] = "?"


def all_routes(paths):  # finds next available room
    directions = []
    for path in paths:
        if paths[path] == "?":
            directions.append(path)
    return directions



while len(explored) < len(room_graph):
    cur_room = player.current_room
    # if it has not been visited
    if cur_room.id not in explored:
        route(cur_room)
    # get all possible directions
    directions = all_routes(explored[cur_room.id])

    # If there are no unexplored paths
    if len(directions) == 0:
        # BFS to find the closest unexplored path
        path = bfs(explored)
        # record the path taken
        for rooms in path:
            for direction in explored[cur_room.id]:
                # if the room id value for the direction is the same as the room id in the path
                # if the player is not already at the room in the path
                if explored[cur_room.id][direction] == rooms and cur_room.id != rooms:
                    # add direction
                    traversal_path.append(direction)
                    next_room = cur_room.get_room_in_direction(direction)
                    # update visited dict
                    explored[cur_room.id][direction] = next_room.id
                    # if room not visited
                    if next_room.id not in explored:
                        # add room
                        route(next_room)
                    # player previous path
                    prev_room = reverse_direction[direction]
                    # came_from
                    explored[next_room.id][prev_room] = cur_room.id
                    # move player to the next room
                    player.travel(direction)
    else:
        # choose a random direction
        new_route = random.choice(directions)
        traversal_path.append(new_route)
        next_room = cur_room.get_room_in_direction(new_route)
        explored[cur_room.id][new_route] = next_room.id
        # if next room unexplored
        if next_room.id not in explored:
            route(next_room)
        prev_room = reverse_direction[new_route]
        explored[next_room.id][prev_room] = cur_room.id
        player.travel(new_route)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


# hints:
# use DFT then if stuck use BFS - using returned path for BFS to move player not during BFS