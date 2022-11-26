import cv2
import numpy as np
import pickle
from levels import *

PATH = "classes" 

with open(f"{PATH}/classes.pkl", "rb") as fh:
    classes_array = pickle.load(fh)


def manual_classifier(cell):
    temp = np.zeros(len(classes_array))
    for n,i in enumerate(classes_array):
        temp2 = []
        for j in i:
            temp2.append(np.mean(cell - j))
        temp[n] = np.min(temp2)
    return np.argmin(temp)

def mean_classifier(cell):
    return int(cell.mean())


def read_image(path, classifier=manual_classifier):
    image = cv2.imread(path, -1)
    E = np.zeros((15,10), dtype=int)
    for i in range(15):
        for j in range(10):
            cell = image[64*i:64*(i+1),64*j:64*(j+1)]
            E[i, j] = classifier(cell)
    return E

def getLvl(level):
    stage = 1
    levels = [l01, l02, l03, l04, l05, l06, l07, l08, l09, l10,
                 l11, l12, l13, l14, l15, l16, l17, l18, l19, l20]
    for lv in levels:
        count = 0
        for i in range(len(level)):
            for j in range(len(level[0])):
                if(level[i][j] == lv[i][j]):
                    count +=1
        if(count >= 147):
           return stage        
        stage += 1
    return ''


if __name__ == '__main__':
    ENVIRONMENT = read_image("lvls/l15.png", manual_classifier)
    print(ENVIRONMENT)

