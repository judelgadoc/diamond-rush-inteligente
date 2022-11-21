import grabber
import map_reader
import movement
import time
import numpy as np

grabber.start()

MAP = map_reader.read_image("E:/Downloads/Diamond/download.png")
print(MAP)
nPMap = np.array(MAP)
x=MAP.flatten().tolist()
index = x.index(6)
position = np.unravel_index(index,MAP.shape)
position = (position[0],position[1], False, False)
x = 0
y = 0
moves = movement.findBestPathToNextGem(nPMap, position)
time.sleep(1)
moves = "right,down,down,down,down,down,down,left,down,down,right,right,right,right,right,right,down,right,up,up,left,left,down,left,left".split(",")
for move in moves:
    
    swapIndex = movement.setMove(move, position)    
    dataOut = MAP[swapIndex[0]][swapIndex[1]]
    canMove = movement.verifyColission(dataOut, position)
    if(canMove):
        swapResult = movement.swap(MAP, position, swapIndex)
        position = swapResult[1]
        movement.signalMove(move)
    print('-------------------------------------------------------------------------')
    print(MAP)


