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
        if self.parent is not None and other.parent is not None:
            return self.position == other.position and self.f == other.f and self.g == other.g and self.h == other.h and self.parent.position == other.parent.position
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

    def pacman_heuristic(self, node):
        distances = []
        distances_diamonds = []
        maze_flat = node.maze.flatten()
        diamonds = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 0)[0]]
        diamonds += [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 15)[0]]
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
    
    def pacman_with_holes_heuristic(self, node):
        distances = []
        distances_holes = []
        maze_flat = node.maze.flatten()
        holes = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 1)[0]]
        for i in holes:
            distance_node_hole = abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] )
            distances.append(distance_node_hole)
            for j in holes:
                distance_hole_hole = abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] )
                distances_holes.append(distance_hole_hole)
        #print("debug_pacman:", distances, distances_diamonds, node)
        return min(distances) + max(distances_holes) if len(distances) else 0  #max(distances_diamonds)

    # piedra más cercana al hueco más cercano
    def rock_to_hole_heuristic(self, node):
        distances = []
        distances_holes = []
        maze_flat = node.maze.flatten()
        holes = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 1)[0]]
        rocks = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 12)[0]]
        closest_rock = rocks[np.array([ abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] ) for i in rocks ]).argmin()]
        closest_hole = holes[np.array([ abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] ) for i in holes ]).argmin()]
        val = np.array([ abs( node.position[0] - i[0] ) + abs( node.position[1] - i[1] ) for i in rocks ]).min()
        return abs( closest_hole[0] - closest_rock[0] ) + abs( closest_hole[1] - closest_rock[1] ) + val

    def heuristic_holes(self, node):
        maze_flat = node.maze.flatten()
        def get_adjs(x, y):
            return [(i + x, j + y) for i,j in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        rocks = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 12)[0]]
        holes = [np.unravel_index(i, node.maze.shape) for i in np.where(maze_flat == 1)[0]]
        distances = []
        distances_holes = []
        for i,j in rocks:
            for k in get_adjs(i, j):
                distances.append(abs( node.position[0] - k[0] ) + abs( node.position[1] - k[1] ))
            for h, o in holes:
                distances_holes.append(abs(i - h) + abs(j - o))
        return min(distances) + max(distances_holes) if len(distances) else 0

    def astar(self):
        t = time.time()
        while len(self.open_list) > 0 and time.time() - t < 600:
            current_node = self.get_current_node()
            # Found the goal CHANGE THIS TO GENERIC
            if current_node.position == self.end_node.position and self.number_of_diamonds_heuristic(current_node) == 0:
                path = []
                current = current_node
                while current is not None and current.move is not None:
                    path.append(current.move)
                    current = current.parent
                print("Solution length:", len(path))
                print("Simulated map:", current_node.maze, sep="\n")
                return path[::-1] # Return reversed path
    
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
    
                # Create the f, g, and h values
                child.g = current_node.g + 1
                #child.h = min(self.pacman_heuristic(child), self.number_of_holes_heuristic(child))
                #child.h = self.number_of_holes_heuristic(child)
                #child.h = self.pacman_with_holes_heuristic(child)
                child.h = max(self.heuristic_holes(child), self.number_of_holes_heuristic(child))
                child.h = min(child.h, self.pacman_heuristic(child))
                #child.h = self.pacman_heuristic(child)
                #child.h = 0
                child.h *= 1 + 0.1/100
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
        print("Final position:", current_node.position)
        print("Simulated map:", current_node.maze, sep="\n")
        return path[::-1] # Return reversed path

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
    MAP = map_reader.read_image("lvls/l04.png")
    
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
    
    
