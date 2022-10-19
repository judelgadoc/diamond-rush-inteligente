import cv2
import numpy as np
import os
import pickle
from cell_saver_lvls import *

PATH = os.getcwd() + "/classes"

classes = ['diamante',
 'hueco',
 'lava',
 'llave',
 'meta',
 'pared',
 'personaje',
 'piso',
 'puas',
 'puerta',
 'puerta_metalica',
 'reliquia',
 'roca',
 'switch']

def save_lvl(img_path, img_matrix, name):
    image = cv2.imread(img_path, -1)
    for i in range(15):
        for j in range(10):
            cell = image[64*i:64*(i+1),64*j:64*(j+1)]
            cell_class = classes[img_matrix[i][j]]
            cv2.imwrite(f"{PATH}/{cell_class}/{name}-{i}_{j}.png", cell)

def load_classes():
    ans = []
    for i in classes:
        temp = [cv2.imread(f"{PATH}/{i}/{c}", -1) for c in os.listdir(f"{PATH}/{i}")]
        ans.append(temp)
    return ans

def export_classes():
    fh = open(f"{PATH}/classes.pkl", "wb")
    pickle.dump(classes_array, fh, pickle.HIGHEST_PROTOCOL)
    fh.close()

save_lvl("lvls/l02.png", l02, "l02")
save_lvl("lvls/l03.png", l03, "l03")
save_lvl("lvls/l08.png", l08, "l08")

classes_array = load_classes()

export_classes()
