import grabber
import map_reader
import movement
import time
import numpy as np

def walls(i, j):
    ans = []
    if i > 0 and MAP[i - 1][j] != 5:
        ans.append("up")
    if i < 14 and MAP[i + 1][j] != 5:
        ans.append("down")
    if j > 0 and MAP[i][j - 1] != 5:
        ans.append("left")
    if j < 10 and MAP[i][j + 1] != 5:
        ans.append("right")
    return ans

#MAP = map_reader.read_image("lvls/l01.png")
MAP = map_reader.read_image("/tmp/download.png")

def get_indy_position():
    temp=MAP.flatten().tolist()
    index = temp.index(6)
    return np.unravel_index(index,MAP.shape)


print("THE MAP IS:\n", MAP)
print("INDY IS IN THE FOLLOWING COORDINATE:", get_indy_position())

p = get_indy_position()
print(walls(p[0], p[1]))







