import grabber
import map_reader
import movement
import time
import numpy as np


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, move=None):
        self.parent = parent
        self.position = position
        self.move = move

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return str((self.position, self.g, self.h, self.f))


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None and current.move is not None:
                path.append(current.move)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in get_allowed_moves(current_node.position[0],current_node.position[1]): # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range 
            #is_in_range = node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0
            #is_walkable = maze[node_position[0]][node_position[1]] != 5

            # Create new node
            new_node = Node(current_node, node_position, new_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)

def path_as_actions(path):
    ans = []
    for i in path:
        if i == (-1, 0):
            temp = "up"
        elif i == (1, 0):
            temp = "down"
        elif i == (0, -1):
            temp = "left"
        elif i == (0, 1):
            temp = "right"
        else:
            temp = "No autoriso"
        ans.append(temp)
    return ans


def walls(i, j):
    ans = []
    if i > 0 and MAP[i - 1][j] != 5:
        ans.append("up")
    if i < 14 and MAP[i + 1][j] != 5:
        ans.append("down")
    if j > 0 and MAP[i][j - 1] != 5:
        ans.append("left")
    if j < 10 and MAP[i][j + 1] != 5:
        ans.append("right")
    return ans

def get_allowed_moves(i, j):
    ans = []
    if i > 0 and MAP[i - 1][j] != 5:
        ans.append((-1, 0))
    if i < 14 and MAP[i + 1][j] != 5:
        ans.append((1, 0))
    if j > 0 and MAP[i][j - 1] != 5:
        ans.append((0, -1))
    if j < 10 and MAP[i][j + 1] != 5:
        ans.append((0, 1))
    return ans

def get_indy_position():
    temp=MAP.flatten().tolist()
    index = temp.index(6)
    return np.unravel_index(index,MAP.shape)


def get_goal_position():
    temp=MAP.flatten().tolist()
    index = temp.index(4)
    return np.unravel_index(index,MAP.shape)

if __name__ == '__main__':
    MAP = map_reader.read_image("lvls/l02.png")
    #MAP = map_reader.read_image("/tmp/download.png")
    
    p = get_indy_position()
    goal = get_goal_position()
    
    print("THE MAP IS:\n", MAP)
    print("INDY IS IN THE FOLLOWING COORDINATE:", p)
    print("THE GOAL IS IN THE FOLLOWING COORDINATE:", goal)
    
    
    print(walls(p[0], p[1]))
    print(get_allowed_moves(p[0], p[1]))
    
    print(get_allowed_moves(9, 2))
    
    path = astar(MAP, p, goal)
    
    
    path = path_as_actions(path)
    print(path)
    
