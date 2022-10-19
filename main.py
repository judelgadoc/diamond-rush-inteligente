import grabber
import map_reader
import movement
import time
import numpy as np

grabber.start()

MAP = map_reader.read_image("/home/judelgadoc/Downloads/download.png")
print(MAP)

x=MAP.flatten().tolist()
index = x.index(6)
position = np.unravel_index(index,MAP.shape)
x = 0
y = 0
j = position[0]
i = position[1]
time.sleep(1)
moves = "up up down down left right left right right right right".split(" ")
for move in moves:
    swapIndex = movement.setMove(move)
    MAP = movement.swap(MAP, position, swapIndex)
    position = swapIndex
    x = 0
    y = 0
    j = position[0]
    i = position[1]
    movement.signalMove(move)
    print('-------------------------------------------------------------------------')
    print(MAP)
