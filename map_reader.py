import cv2
import numpy as np
import pickle

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


if __name__ == '__main__':
    ENVIRONMENT = read_image("lvls/l15.png", manual_classifier)
    print(ENVIRONMENT)
