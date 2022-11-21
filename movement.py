import numpy as np
import pyautogui
import time
import copy
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
position = (position[0],position[1], False, False)

x = 0
y = 0
j = position[0]
i = position[1]

def signalMove(move):
    if move =='up':    
        pyautogui.keyDown('up')
        time.sleep(.05)
        pyautogui.keyUp('up')
    elif move =='down':
        pyautogui.keyDown('down')
        time.sleep(.05)
        pyautogui.keyUp('down')
    elif move =='right':
        pyautogui.keyDown('right')
        time.sleep(.05)
        pyautogui.keyUp('right')
    elif move =='left':
        pyautogui.keyDown('left')
        time.sleep(.05)
        pyautogui.keyUp('left')
    else:
        print("What are you doing? o.O")
    
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

def swap(_MAP, pos_in, pos_out):
    dataIn = _MAP[pos_in[0]][pos_in[1]]
    dataOut = _MAP[pos_out[0]][pos_out[1]] 

    #If the character is on a trap the trap will block the path

    #swapIndex = (pos_x, pos_y, isTrap, hasKey)

    ##if next step is a diamond 
    if (dataOut == 0):
        _MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            _MAP[pos_in[0]][pos_in[1]] = 5
        else:
            _MAP[pos_in[0]][pos_in[1]] = 7
        swapIndex = (pos_out[0], pos_out[1], False, pos_in[3])

    # If nex step is floor
    if (dataOut == 7):
        _MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            _MAP[pos_in[0]][pos_in[1]] = 5
        else:
            _MAP[pos_in[0]][pos_in[1]] = dataOut
        swapIndex = (pos_out[0], pos_out[1], False, pos_in[3])

    #If next step its a trap
    if (dataOut == 8):
        _MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            _MAP[pos_in[0]][pos_in[1]] = 5
        else:
            _MAP[pos_in[0]][pos_in[1]] = 7
        swapIndex = (pos_out[0], pos_out[1], True, pos_in[3])
           
    #If next step its a key
    if (dataOut == 3):
        _MAP[pos_out[0]][pos_out[1]] = dataIn
        if (pos_in[2]):
            _MAP[pos_in[0]][pos_in[1]] = 5
        else:
            MAP[pos_in[0]][pos_in[1]] = 7
        swapIndex = (pos_out[0], pos_out[1], False, True)

    #If next step is a wall
    if (dataOut == 5):
        _MAP[pos_out[0]][pos_out[1]] = dataOut
        _MAP[pos_in[0]][pos_in[1]] = dataIn
        swapIndex = (pos_in[0], pos_in[1], False, pos_in[3])

    #If nex step is lava
    if (dataOut == 2):
        _MAP[pos_out[0]][pos_out[1]] = dataOut
        _MAP[pos_in[0]][pos_in[1]] = dataIn    
        swapIndex = (pos_in[0], pos_in[1], False, pos_in[3])

    #If nex step is blocking door
    if (dataOut == 9):
        #If has key
        if (pos_in[3]):       
            _MAP[pos_out[0]][pos_out[1]] = dataIn
            if (pos_in[2]):
                _MAP[pos_in[0]][pos_in[1]] = 5
            else:
                _MAP[pos_in[0]][pos_in[1]] = 7
            swapIndex = (pos_out[0], pos_out[1], False, False)
        else:
            _MAP[pos_out[0]][pos_out[1]] = dataOut
            _MAP[pos_in[0]][pos_in[1]] = dataIn    
            swapIndex = (pos_in[0], pos_in[1], False, pos_in[3])

    return (_MAP, swapIndex)

def findBestPathToNextGem(MAP, pos_in):
    originalMAP = copy.copy(MAP)
    val = 0
    totalMoves = []
    index = np.where(MAP==val)
    while len(index[0] > 0):
        index = np.where(MAP==val)
        moves = []
        for i in range(len(index[0])):
            result = findNextSteps(originalMAP, pos_in, index[0][i], index[1][i])
            moves.append(result[1])
        min =[]
        for movesList in moves:
            min = len(movesList)
            if(len(min) <= len(movesList)):
                min = movesList
        for move in min:
            totalMoves.append(move)   

    return totalMoves

def findNextSteps(MAP, pos_in, y, x):
    moves = []
    possibleMoves = []
    bestWay = False    
    newMAP = copy.copy(MAP)
    while (( pos_in[0] == y and pos_in[1] == x) == False):
        if(len(moves) > 0):
            lastMove = moves[len(moves) - 1]
        else:
            lastMove = ''
        if(len(moves)>1):
            penultMove = moves[len(moves)-2]
        else:
            penultMove = ''
        #try up
        if(lastMove != "down" and (lastMove == "left" and penultMove == "down") is not True):
            swapIndex = [pos_in[0]-1,pos_in[1]]
            dataOut = newMAP[swapIndex[0]][swapIndex[1]]
            canMove = verifyColission(dataOut, pos_in)
            if canMove:
                moves.append("up")
                swapResult = swap(newMAP, pos_in, swapIndex)
                pos_in = swapResult[1]
                newMAP = swapResult[0]
                print('-------------------------------------------------------------------------')
                print(newMAP)
                continue
            
        if(lastMove != "up" and (lastMove == "left" and penultMove == "up")is not True):
          #try down
            swapIndex = [pos_in[0]+1,pos_in[1]]
            dataOut = newMAP[swapIndex[0]][swapIndex[1]]
            canMove = verifyColission(dataOut, pos_in)
            if canMove:
                moves.append("down")
                swapResult = swap(newMAP, pos_in, swapIndex)
                pos_in = swapResult[1]
                newMAP = swapResult[0]
                print('-------------------------------------------------------------------------')
                print(newMAP)
                continue

        if(lastMove != "right"):
            #try left
            swapIndex = (pos_in[0],pos_in[1]-1)
            dataOut = newMAP[swapIndex[0]][swapIndex[1]]
            canMove = verifyColission(dataOut, pos_in)
            if canMove:
                moves.append("left")
                swapResult = swap(newMAP, pos_in, swapIndex)
                pos_in = swapResult[1]
                newMAP = swapResult[0]
                print('-------------------------------------------------------------------------')
                print(newMAP)
                continue

        if(lastMove != "left"):
          #try right
            swapIndex = [pos_in[0],pos_in[1]+1]
            dataOut = newMAP[swapIndex[0]][swapIndex[1]]
            canMove = verifyColission(dataOut, pos_in)
            if canMove:
                moves.append("right")
                swapResult = swap(newMAP, pos_in, swapIndex)
                pos_in = swapResult[1]
                newMAP = swapResult[0]
                print('-------------------------------------------------------------------------')
                print(newMAP)
                continue
     
    print('-------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------')   
    return (newMAP, moves)

if __name__ == '__main__':
    time.sleep(1)
    nPMap = np.array(MAP)
    moves = findBestPathToNextGem(nPMap, position)
    moves = "up up down down left right left right".split(" ")
    for move in moves:
        swapIndex = setMove(move, position)
        MAP = swap(MAP, position, swapIndex)
        position = swapIndex
        x = 0
        y = 0
        j = position[0]
        i = position[1]
        signalMove(move)
        print('-------------------------------------------------------------------------')
        print(MAP)


