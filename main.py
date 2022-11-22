import grabber
import map_reader
import movement
import solver
import time
import numpy as np

grabber.start()


MAP = map_reader.read_image("/tmp/download.png")
    
MAP_as_list = MAP.flatten().tolist()
p = np.unravel_index(MAP_as_list.index(6), MAP.shape)
goal = np.unravel_index(MAP_as_list.index(4), MAP.shape)
#goal = (7, 6)    
print("THE MAP IS:\n", MAP)
print("INDY IS IN THE FOLLOWING COORDINATE:", p)
print("THE GOAL IS IN THE FOLLOWING COORDINATE:", goal)
    
s = solver.Solver(MAP, p, goal)
path = s.get_path()
path = s.get_path_as_actions()
print(path)

moves = path

for move in moves:
    movement.signalMove(move)
