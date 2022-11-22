import grabber
import map_reader
import movement
import time
import numpy as np


class Node:
    def __init__(self, parent=None, position=None, move=None, maze=None):
        self.parent = parent
        self.position = position
        self.move = move
        self.maze = maze.copy()

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position and self.f == other.f and self.g == other.g and self.h == other.h

    def __repr__(self):
        if self.parent is not None:
            return "<{}, g={}, h={}, f={}, p={}>".format(self.position, self.g, self.h, self.f, self.parent.position)
        else:
            return "<{}, g={}, h={}, f={}>".format(self.position, self.g, self.h, self.f)

class Solver:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start_node = Node(None, start, maze=self.maze)
        self.start_node.g = self.start_node.h = self.start_node.f = 0
        self.end_node = Node(None, end, maze=self.maze)
        self.end_node.g = self.end_node.h = self.end_node.f = 0

        self.open_list = []
        self.closed_list = []

        self.open_list.append(self.start_node)
        self.path = []

    def get_current_node(self):
        current_node = self.open_list[0]
        current_index = 0
        for index, item in enumerate(self.open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        self.open_list.pop(current_index)
        self.closed_list.append(current_node)
        return current_node

    def get_path(self):
        if len(self.path) == 0:
            self.path = self.astar()
        return self.path

    def get_path_as_actions(self):
        ans = []
        actions_map = {(-1, 0): "up", (1, 0): "down", (0, -1): "left", (0, 1): "right"}
        path = self.get_path()
        for i in path:
            ans.append(actions_map[i])
        return ans

    def manhattan_heuristic(self, node):
        return abs((node.position[0] - self.end_node.position[0])) + abs((node.position[1] - self.end_node.position[1]))

    def pacman_heuristic(self, node):
        distances = []
        distances_diamonds = []
        maze_flat = node.maze.flatten()
        diamonds = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 0)[0]]
        for i in diamonds:
            distance_node_diamond = abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] )
            distances.append(distance_node_diamond)
            for j in diamonds:
                distance_diamond_diamond = abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] )
                distances_diamonds.append(distance_diamond_diamond)
        #print("debug_pacman:", distances, distances_diamonds, node)
        return min(distances) + max(distances_diamonds) if len(distances) else 0  #max(distances_diamonds)

    def number_of_diamonds_heuristic(self, node):
        maze_flat = node.maze.flatten()
        return len([np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 0)[0]])

    def astar(self):
        while len(self.open_list) > 0:
            current_node = self.get_current_node()

            # Found the goal
            if current_node.position == self.end_node.position and current_node.h == 0:
                path = []
                current = current_node
                while current is not None and current.move is not None:
                    path.append(current.move)
                    current = current.parent
                print("Solution length:", len(path))
                return path[::-1] # Return reversed path
    
            # Generate children
            children = []
            for new_position in get_allowed_moves(current_node.position[0], current_node.position[1]):
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                new_node = Node(current_node, node_position, new_position, maze=current_node.maze)
                if new_node.maze[node_position[0]][node_position[1]] == 0:
                    new_node.maze[node_position[0]][node_position[1]] = 7
                children.append(new_node)
    
            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in self.closed_list if closed_child == child]) > 0:
                    continue
    
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = self.pacman_heuristic(child)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in self.open_list if child == open_node]) > 0:
                    continue
    
                self.open_list.append(child)
        # didn't found the path but at least return the incomplete result
        path = []
        current = current_node
        while current is not None and current.move is not None:
            path.append(current.move)
            current = current.parent
        print("Failed solution length:", len(path))
        return path[::-1] # Return reversed path


def get_diamonds(maze):
    maze_flat = maze.flatten()
    return len([np.unravel_index(i, maze.shape) for i in np.where(maze_flat == 0)[0]])

def get_allowed_moves(i, j):
    ans = []
    if i > 0 and MAP[i - 1][j] != 5:
        ans.append((-1, 0)) # up
    if i < 14 and MAP[i + 1][j] != 5:
        ans.append((1, 0)) # down
    if j > 0 and MAP[i][j - 1] != 5:
        ans.append((0, -1)) # left
    if j < 10 and MAP[i][j + 1] != 5:
        ans.append((0, 1)) # right
    return ans


if __name__ == '__main__':
    MAP = map_reader.read_image("lvls/l02.png")
    
    MAP_as_list = MAP.flatten().tolist()
    p = np.unravel_index(MAP_as_list.index(6), MAP.shape)
    goal = np.unravel_index(MAP_as_list.index(4), MAP.shape)
    MAP_flat = MAP.flatten()
    print([np.unravel_index(i, MAP.shape) for i in np.where(MAP_flat == 0)[0]])
    
    print("THE MAP IS:\n", MAP)
    print("INDY IS IN THE FOLLOWING COORDINATE:", p)
    print("THE GOAL IS IN THE FOLLOWING COORDINATE:", goal)
    
    s = Solver(MAP, p, goal)
    path = s.get_path()
    print(path)
    path = s.get_path_as_actions()
    print(path)
    
    
