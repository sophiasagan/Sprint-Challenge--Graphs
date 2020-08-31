from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

import collections
import itertools

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

traversal_path = []

reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# backtrack
reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# compute all possible routes

all_routes = [[
    # top 4 lines produce lowest so far of 925
    ['e', 'n', 'w', 's'], 
    ['e', 'w', 's', 'n'],
    ['w', 's', 'n', 'e'], 
    ['n', 'w', 'e', 's'],
    # ['n', 'e', 's', 'w'], 
    # ['n', 'e', 'w', 's'],
    # ['n', 's', 'e', 'w'], 
    # ['n', 's', 'w', 'e'],
    # ['n', 'w', 's', 'e'], 
    # ['e', 'n', 's', 'w'],
    # ['e', 's', 'n', 'w'], 
    # ['e', 's', 'w', 'n'],
    # ['s', 'n', 'e', 'w'], 
    # ['s', 'n', 'w', 'e'],
    # ['s', 'e', 'n', 'w'], 
    # ['s', 'e', 'w', 'n'],
    # ['s', 'w', 'n', 'e'], 
    # ['s', 'w', 'e', 'n'],
    # ['w', 'n', 'e', 's'], 
    # ['w', 'n', 's', 'e'],
    # ['w', 'e', 'n', 's'], 
    # ['w', 'e', 's', 'n'],
    # ['w', 's', 'e', 'n'], 
    # ['e', 'w', 'n', 's']
]]

# all_routes = permutations(['n', 'e', 's', 'w'])

# for r in list(all_routes):
#     print(r)


# threshold splits maze in half allowing search based on area
def search(total_rooms=500, split_threshold=14):

    for route in all_routes:
        # reset variables 
        cur_path = []
        maze = dict()

        while True:
            # peeking for looking ahead in route w/o traversing
            peek = False
            explored = False
            cur_room = player.current_room
            dx = abs(cur_room.x)
            dy = abs(cur_room.y)
            
            # dx = abs(cur_room.x - (len(maze)))
            # dy = abs(cur_room.y - (len(maze)))

            if cur_room.id not in maze:
                maze[cur_room.id] = {
                    cur_direction: '?' for cur_direction in cur_room.get_exits()}
                # reached end
                if len(maze) == total_rooms:
                    break

            if len(maze) > 1:
                maze[prev_room][next_room] = cur_room.id
                maze[cur_room.id][prev_path] = prev_room

            # heuristics - https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
            # pulls specific route based on cur_room coordinates
            if (dx) >= (split_threshold - 1) and (dy) >= split_threshold:
                area = 0 
            elif (dx) >= split_threshold and (dy) < split_threshold:
                area = 1 
            elif (dy) <= split_threshold and (dx) < (split_threshold - 2):
                area = 2 
            elif (dy) < (split_threshold -2) and (dx) >= split_threshold:
                area = 3 

            
            # if dx > 0 and abs(dx) - abs(dy) > split_threshold:
            #     area = 0
            # elif dx < 0 and abs(dx) - abs(dy) > split_threshold:
            #     area = 1
            # elif dy > 0 and abs(dy) - abs(dx) > split_threshold:
            #     area = 2
            # elif dy < 0 and abs(dy) - abs(dx) > split_threshold:
            #     area = 3
            
            # peeking to find room with at least one exit in unexplored path based on current area
            for cur_direction in route[area]:
                if cur_direction in maze[cur_room.id] and maze[cur_room.id][cur_direction] == '?' and len(cur_room.get_room_in_direction(cur_direction).get_exits()) == 1:
                    next_room = cur_direction
                    peek = True
                    explored = True
                    break
            
            if peek == False:
                for cur_direction in route[area]:
                    if cur_direction in maze[cur_room.id] and maze[cur_room.id][cur_direction] == '?':
                        next_room = cur_direction
                        explored = True
                        break

            # bfs
            if explored == False:
                visited = set()
                q = Queue()
                q.enqueue([player.current_room.id])

                while q.size() > 0:
                    path = q.dequeue()
                    room = path[-1]

                    # If '?' is found - follow the path
                    if '?' in maze[room].values():
                        # Stop in the room just before the room with the '?'
                        for cur_direction in range(len(path) - 2):
                            cur_path.append(path[cur_direction])
                            player.travel(path[cur_direction])
                        next_room = path[-2]
                        break

                    if room not in visited:
                        visited.add(room)
                        for cur_direction, id in maze[room].items():
                            next_path = list(path)
                            next_path[-1] = cur_direction
                            next_path.append(id)
                            q.enqueue(next_path)

            prev_room = player.current_room.id
            prev_path = reverse[next_room]

            # Add next direction to the traversal path
            cur_path.append(next_room)
            player.travel(next_room)

    return cur_path


traversal_path = search(len(room_graph))
# print(traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == 'q':
#         break
#     else:
#         print("I did not understand that command.")


# Helps:


# https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
# https://www.redblobgames.com/pathfinding/a-star/implementation.py
