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
        #if self.parent is not None and other.parent is not None:
        #    return self.position == other.position and self.f == other.f and self.g == other.g and self.h == other.h and self.parent.position == other.parent.position
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

    def get_distance(self, pos1, pos2, func="manhattan"):
        if func == "manhattan":
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        elif func == "euclid_squared":
            return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

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
        temp = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 0)[0]]
        temp += [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 15)[0]]
        return len(temp)

    def number_of_holes_heuristic(self, node):
        maze_flat = node.maze.flatten()
        return len([np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 1)[0]])
    
    def holes_heuristic(self, node):
        # TODO: Add the whatsapp explanation
        maze_flat = node.maze.flatten()
        def get_adjs(x, y):
            return [(i + x, j + y) for i,j in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        rocks = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 12)[0]]
        rocks += [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 15)[0]]
        holes = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 1)[0]]
        if len(holes) == 0:
            print("debug map:", node.maze, sep="\n")
            a = {(-1, 0): "up", (1, 0): "down", (0, -1): "left", (0, 1): "right"}
            path = [a[i] for i in self.get_node_path(node)]
            print("debug_path:", path)
            return 0
        closest_rock = rocks[np.array([ abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] ) for i in rocks ]).argmin()]
        closest_hole_to_rock = holes[np.array([ abs( closest_rock[0] - i[0] ) + abs( closest_rock[1] - i[1] ) for i in holes ]).argmin()]
        adjs = get_adjs(closest_rock[0], closest_rock[1])
        furthest_adj_to_hole = adjs[np.array([ self.get_distance(i, closest_hole_to_rock) for i in adjs ]).argmax()]
        return self.get_distance(closest_rock, closest_hole_to_rock) + self.get_distance(node.position, furthest_adj_to_hole)

    def general_heuristic(self, node):
        maze_flat = node.maze.flatten()
        holes = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 1)[0]]
        if len(holes) > 0:
            print("debug: using holes heuristic")
            return self.holes_heuristic(node)
        else:
            print("debug: using pacman heuristic")
            print("debug map:", node.maze, sep="\n")
            a = {(-1, 0): "up", (1, 0): "down", (0, -1): "left", (0, 1): "right"}
            path = [a[i] for i in self.get_node_path(node)]
            print("debug_path:", path)
            #node.g = 0
            return self.pacman_heuristic(node)

    def get_node_path(self, node):
        path = []
        current = node
        while current is not None and current.move is not None:
            path.append(current.move)
            current = current.parent
        return path[::-1] # Return reversed path


    def astar(self):
        heuristic_changed = False
        t = time.time()
        while len(self.open_list) > 0 and time.time() - t < 20:
            current_node = self.get_current_node()
            if current_node.position == self.end_node.position and self.number_of_diamonds_heuristic(current_node) == 0:
            #if self.number_of_holes_heuristic(current_node) == 0:
                path = self.get_node_path(current_node)
                print("Simulated map:", current_node.maze, sep="\n")
                print("Solution length:", len(path))
                return path
            # Generate children
            children = []
            for new_position in get_allowed_moves(current_node.position[0], current_node.position[1], current_node.maze):
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                new_node = Node(current_node, node_position, new_position, maze=current_node.maze)
                new_node.maze = maze_transition(new_node.maze, node_position, new_position)
                children.append(new_node)
    
            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in self.closed_list if closed_child == child]) > 0:
                    continue
                #maze_flat = current_node.maze.flatten()
                #holes = [np.unravel_index(i, current_node.maze.shape) for i in np.where(maze_flat == 1)[0]]
                #if len(holes) == 0 and not heuristic_changed:
                #    self.closed_list = []
                #    current_node.g = 0
                #    self.open_list = [current_node]
                #    heuristic_changed = True

                # Create the f, g, and h values
                child.g = current_node.g + 1
                #child.h = self.general_heuristic(child)
                child.h = max(self.pacman_heuristic(child), self.holes_heuristic(child))
                child.h *= (1 + 1/1000)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in self.open_list if child == open_node]) > 0:
                    continue
    
                self.open_list.append(child)
        # didn't found the path but at least return the incomplete result
        path = self.get_node_path(child)
        print("Simulated map:", child.maze, sep="\n")
        print("Failed solution length:", len(path))
        return path




def maze_transition(maze, position, move):
    """
    How changes the maze when the player moves into position (i, j)
    """
    i, j = position
    x, y = move
    if maze[i][j] == 0:
        maze[i][j] = 7
    elif maze[i][j] == 8:
        maze[i][j] = 5
    elif maze[i][j] == 12:
        if maze[i + x][j + y] == 1:
            maze[i][j] = 7
            maze[i + x][j + y] = 7
        elif maze[i + x][j + y] == 7:
            maze[i][j] = 7
            maze[i + x][j + y] = 12
        elif maze[i + x][j + y] == 0:
            maze[i][j] = 7
            maze[i + x][j + y] = 15 # temporal state "diamond under rock"
    elif maze[i][j] == 15:
        if maze[i + x][j + y] == 1:
            maze[i][j] = 7
            maze[i + x][j + y] = 7
        elif maze[i + x][j + y] == 7:
            maze[i][j] = 7
            maze[i + x][j + y] = 12
        elif maze[i + x][j + y] == 0:
            maze[i][j] = 7
            maze[i + x][j + y] = 15 # temporal state "diamond under rock"
    return maze


def get_allowed_moves(i, j, maze):
    ans = []
    not_allowed = [5, 2, 1]
    rock_condition_up = maze[i - 1][j] != 12 or (maze[i - 1][j] == 12 and maze[i - 2][j] != 5)
    rock_condition_down = maze[i + 1][j] != 12 or (maze[i + 1][j] == 12 and maze[i + 2][j] != 5)
    rock_condition_left = maze[i][j - 1] != 12 or (maze[i][j - 1] == 12 and maze[i][j - 2] != 5)
    rock_condition_right = maze[i][j + 1] != 12 or (maze[i][j + 1] == 12 and maze[i][j + 2] != 5)
    #print(rock_condition_up, rock_condition_down, rock_condition_left, rock_condition_right)
    if i > 0 and maze[i - 1][j] not in not_allowed and rock_condition_up:
        ans.append((-1, 0)) # up
    if i < 14 and maze[i + 1][j] not in not_allowed and rock_condition_down:
        ans.append((1, 0)) # down
    if j > 0 and maze[i][j - 1] not in not_allowed and rock_condition_left:
        ans.append((0, -1)) # left
    if j < 10 and maze[i][j + 1] not in not_allowed and rock_condition_right:
        ans.append((0, 1)) # right
    return ans


if __name__ == '__main__':
    maps = ["{:02d}".format(i) for i in [4]]
    for i in maps:
        print(f"LVL {i}")
        MAP = map_reader.read_image(f"lvls/l{i}.png")
        
        MAP_as_list = MAP.flatten().tolist()
        p = np.unravel_index(MAP_as_list.index(6), MAP.shape)
        try:
            goal = np.unravel_index(MAP_as_list.index(4), MAP.shape)
        except:
            goal = np.unravel_index(MAP_as_list.index(11), MAP.shape)
        print("THE MAP IS:\n", MAP)
        print("INDY IS IN THE FOLLOWING COORDINATE:", p)
        print("THE GOAL IS IN THE FOLLOWING COORDINATE:", goal)
        
        s = Solver(MAP, p, goal)
        path = s.get_path()
        path = s.get_path_as_actions()
        print(path)
    
    
