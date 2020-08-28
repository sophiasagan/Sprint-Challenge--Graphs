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
visited_path = {}
reverse_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

def route(room):  # start route
    visited_path[room.id] = {}
    for next_room in room.get_exits():
        visited_path[room.id][next_room] = "?"


def search(paths):  # finds next available room
    directions = []
    for path in paths:
        if paths[path] == "?":
            directions.append(path)
    return directions


def bfs(explored):  # returns a path to the closest unexplored path
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


while len(visited_path) < len(room_graph):
    # if it has not been visited
    if player.current_room.id not in visited_path:
        route(player.current_room)
    # get all possible directions
    directions = search(visited_path[player.current_room.id])

    # If there are no unexplored paths
    if len(directions) == 0:
        # BFS to find the closest unexplored path
        path = bfs(visited_path)
        # record the path taken
        for room_id in path:
            # players current room id
            cur_room_id = player.current_room.id

            for direction in visited_path[cur_room_id]:
                # if the room id value for the direction is the same as the room id in the path
                # AND if the player is not already at the room in the path
                if visited_path[cur_room_id][direction] == room_id and cur_room_id != room_id:
                    # add direction
                    traversal_path.append(direction)
                    next_room = player.current_room.get_room_in_direction(
                        direction)
                    # update visited key value pair
                    visited_path[cur_room_id][direction] = next_room.id
                    # if room not visited
                    if next_room.id not in visited_path:
                        route(next_room)
                    # player previous path
                    prev_room = reverse_direction[direction]
                    # came_from
                    visited_path[next_room.id][prev_room] = cur_room_id
                    # move player to the next room
                    player.travel(direction)
    else:
        # choose a random direction
        new_route = random.choice(directions)
        traversal_path.append(new_route)
        next_room = player.current_room.get_room_in_direction(new_route)
        visited_path[player.current_room.id][new_route] = next_room.id
        if next_room.id not in visited_path:
            route(next_room)
        prev_room = reverse_direction[new_route]
        visited_path[next_room.id][prev_room] = player.current_room.id
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