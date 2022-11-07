import numpy as np
import pyautogui
import time
from cell_saver_lvls import *

MAP = np.array([[5, 5, 5, 8, 8, 5, 8, 5, 5, 5],
                 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                 [5, 8, 8, 0, 8, 8, 5, 5, 5, 5],
                 [5, 8, 0, 8, 0, 8, 5, 5, 5, 5],
                 [5, 8, 5, 5, 5, 8, 5, 5, 8, 5],
                 [5, 0 ,5, 5, 5, 0, 8, 0, 8, 5],
                 [5, 0 ,5, 5, 5, 0, 8, 0, 8, 5],
                 [5, 8 ,5, 5, 5, 8, 5, 5, 5, 5],
                 [5, 8 ,5, 8, 0, 8, 5, 5, 5, 5],
                 [5, 8 ,5, 5, 5, 8, 5, 5, 5, 5],
                 [5, 8 ,5, 5, 5, 8, 8, 8, 8, 5],
                 [5, 0, 0, 8, 8, 8, 8, 6, 8, 5],
                 [5, 0, 0, 5, 5, 8, 8, 8, 8, 5],
                 [5, 5 ,5, 5, 5, 5, 5, 5, 5, 5]])

MAP = np.array(l02)

#print(MAP)
x=MAP.flatten().tolist()
index = x.index(6)
position = np.unravel_index(index,MAP.shape)

x = 0
y = 0
j = position[0]
i = position[1]
# time.sleep(1)
# pyautogui.keyDown('alt')
# time.sleep(.2)
# pyautogui.press('tab')
# time.sleep(.2)
# pyautogui.keyUp('alt')
# time.sleep(0.5)
# pyautogui.keyDown('up')
# time.sleep(0.1)
# pyautogui.keyUp('up')

def signalMove(move):
    if move =='up':    
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
    elif move =='down':
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
    elif move =='right':
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')
    elif move =='left':
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
    else:
        print("What are you doing? o.O")
    time.sleep(0.1)
def setMove(move):
    if(move =='up'):    
        y = j-1
        x = i
    elif(move =='down'):
        y = j +1 
        x = i
    elif(move =='right'):
        x = i+1
        y = j
    elif(move =='left'):
        x = i-1
        y = j

    swapIndex = (y, x)
    return swapIndex

def swap(MAP, pos_in, pos_out):
    dataIn = MAP[pos_in[0]][pos_in[1]]
    dataOut = MAP[pos_out[0]][pos_out[1]]
    MAP[pos_out[0]][pos_out[1]] = dataIn
    MAP[pos_in[0]][pos_in[1]] = dataOut
    return (MAP)


if __name__ == '__main__':
    time.sleep(1)
    moves = "up up down down left right left right".split(" ")
    for move in moves:
        swapIndex = setMove(move)
        MAP = swap(MAP, position, swapIndex)
        position = swapIndex
        x = 0
        y = 0
        j = position[0]
        i = position[1]
        signalMove(move)
        print('-------------------------------------------------------------------------')
        print(MAP)


