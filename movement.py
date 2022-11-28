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
       # time.sleep(.135)
        pyautogui.keyUp('up')
    elif move =='down':
        pyautogui.keyDown('down')
      #  time.sleep(.135)
        pyautogui.keyUp('down')
    elif move =='right':
        pyautogui.keyDown('right')
     #   time.sleep(.135)
        pyautogui.keyUp('right')
    elif move =='left':
        pyautogui.keyDown('left')
    #    time.sleep(.135)
        pyautogui.keyUp('left')
    else:
        print("What are you doing? o.O")
    time.sleep(.1)
    
def setMove(move, position):
        
    x = 0
    y = 0
    if(move =='up'):    
        y = position[0] - 1
        x = position[1]
    elif(move =='down'):
        y = position[0] + 1 
        x = position[1]

    elif(move =='right'):
        x = position[1] + 1
        y = position[0]

    elif(move =='left'):
        x = position[1] - 1
        y = position[0]

    swapIndex = (y, x, position[2], position[3])
    return swapIndex

def verifyColission(dataOut, position):
    result = False
    ##if next step is a diamond
    if (dataOut == 0):
        result = True
    # If nex step is floor   
    if (dataOut == 7):
        result = True
    #If next step its a trap
    if (dataOut == 8):
        result = True        
    #If next step its a key
    if (dataOut == 3):
        result = True
    #If next step is a wall
    if (dataOut == 5):
        result = False 
    #If nex step is lava
    if (dataOut == 2):
        result = False 
    #If next step is blocking door
    if (dataOut == 9):
        #If character has collected a key
        if (position[3]):
            result = True
        else: 
            result = False   
    return result

def swap(MAP, pos_in, pos_out):
    dataIn = MAP[pos_in[0]][pos_in[1]]
    dataOut = MAP[pos_out[0]][pos_out[1]] 

    #If the character is on a trap the trap will block the path

    #swapIndex = (pos_x, pos_y, isTrap, hasKey)

    ##if next step is a diamond 
    if (dataOut == 0):
        MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            MAP[pos_in[0]][pos_in[1]] = 5
        else:
            MAP[pos_in[0]][pos_in[1]] = 7
        swapIndex = (pos_out[0], pos_out[1], False, pos_in[3])

    # If nex step is floor
    if (dataOut == 7):
        MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            MAP[pos_in[0]][pos_in[1]] = 5
        else:
            MAP[pos_in[0]][pos_in[1]] = dataOut
        swapIndex = (pos_out[0], pos_out[1], False, pos_in[3])

    #If next step its a trap
    if (dataOut == 8):
        MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            MAP[pos_in[0]][pos_in[1]] = 5
        else:
            MAP[pos_in[0]][pos_in[1]] = 7
        swapIndex = (pos_out[0], pos_out[1], True, pos_in[3])
           
    #If next step its a key
    if (dataOut == 3):
        MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            MAP[pos_in[0]][pos_in[1]] = 5
        else:
            MAP[pos_in[0]][pos_in[1]] = 7
        swapIndex = (pos_out[0], pos_out[1], False, True)

    #If next step is a wall
    if (dataOut == 5):
        MAP[pos_out[0]][pos_out[1]] = dataOut
        MAP[pos_in[0]][pos_in[1]] = dataIn
        swapIndex = (pos_in[0], pos_in[1], False, pos_in[3])

    #If nex step is lava
    if (dataOut == 2):
        MAP[pos_out[0]][pos_out[1]] = dataOut
        MAP[pos_in[0]][pos_in[1]] = dataIn    
        swapIndex = (pos_in[0], pos_in[1], False, pos_in[3])

    #If nex step is blocking door
    if (dataOut == 9):
        #If has key
        if (pos_in[3]):       
            MAP[pos_out[0]][pos_out[1]] = dataIn
            if (pos_in[2]):
                MAP[pos_in[0]][pos_in[1]] = 5
            else:
                MAP[pos_in[0]][pos_in[1]] = 7
            swapIndex = (pos_out[0], pos_out[1], False, False)
        else:
            MAP[pos_out[0]][pos_out[1]] = dataOut
            MAP[pos_in[0]][pos_in[1]] = dataIn    
            swapIndex = (pos_in[0], pos_in[1], False, pos_in[3])

    return (MAP, swapIndex)


if __name__ == '__main__':
    time.sleep(1)
    # lvl04
    #moves = ['right', 'right', 'right', 'right', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'down', 'right', 'up', 'right', 'down', 'down', 'down', 'right', 'up', 'down', 'left', 'up', 'up', 'right', 'right', 'up', 'right', 'down', 'up', 'up', 'up', 'right', 'left', 'down', 'down', 'down', 'left', 'left', 'down', 'down', 'down', 'up', 'up', 'up', 'right', 'right', 'down', 'down']
    moves = ['right', 'right', 'down', 'down', 'down', 'right', 'down', 'down', 'down', 'left', 'down', 'left', 'left', 'up', 'up', 'up', 'right', 'right', 'up', 'right', 'left', 'up', 'up', 'up', 'down', 'down', 'down', 'right', 'left', 'down', 'up', 'right', 'down', 'down', 'right']
    moves = ['right', 'up', 'right', 'down', 'down', 'down', 'left', 'down', 'down', 'left', 'left', 'down', 'down', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'up', 'up', 'right', 'up', 'up', 'down', 'down', 'left', 'down', 'down', 'right', 'left', 'down', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'left', 'right', 'up', 'up', 'right', 'right', 'right', 'down', 'down', 'down']
    for move in moves:
        signalMove(move)


