import grabber
import map_reader
import movement
import time
import numpy as np

grabber.start()

MAP = map_reader.read_image("E:/Downloads/Diamond/download.png")
print(MAP)

x=MAP.flatten().tolist()
index = x.index(6)
position = np.unravel_index(index,MAP.shape)
x = 0
y = 0
time.sleep(1)
moves = "right,right,right,right,right,down,down,down,left,left,left,left,left,down,down,right,down,right,right,right,down,right".split(",")
for move in moves:
    
    swapIndex = movement.setMove(move, position)    
    dataOut = MAP[swapIndex[0]][swapIndex[1]]
    canMove = movement.verifyColission(dataOut)
    if(canMove):
        MAP = movement.swap(MAP, position, swapIndex)
        position = swapIndex
        movement.signalMove(move)
    print('-------------------------------------------------------------------------')
    print(MAP)
