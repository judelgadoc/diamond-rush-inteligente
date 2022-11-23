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

    def heuristic_holes_old(self, node):
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
