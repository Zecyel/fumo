from typing import List, Tuple
from PIL import Image

# Const

height = 0# 19
width = 0# 27
block_size = 20
half_block_size = block_size // 2

def getMap(img: Image) -> List[List[int]]:
    global height, width
    height = img.height // block_size
    width = img.width // block_size

    ret = [[0] * width for i in range(height)]
    for i in range(height):
        for j in range(width):
            pixel = img.getpixel((j * block_size + half_block_size, i * block_size + half_block_size))
            if pixel == (82, 82, 136):
                ret[i][j] = 1
    return ret

def walkable(map: List[List[int]], pos: Tuple[int, int]) -> bool:
    if pos[0] < 0 or pos[0] >= height or pos[1] < 0 or pos[1] >= width:
        return False
    if map[pos[0]][pos[1]] == 1:
        return False
    return True

def dfs(map: List[List[int]], pos: tuple[int, int]) -> Tuple[bool, List[Tuple[int, int]]]:
    if pos[0] == height - 2 and pos[1] == width - 1:
        return True, [pos]
    if not walkable(map, pos):
        return False, []
    
    # print('Reaching..', pos)
    map[pos[0]][pos[1]] = 1
    dire = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for i in dire:
        new_pos = (pos[0] + i[0], pos[1] + i[1])
        ret = dfs(map, new_pos)
        if ret[0]:
            return True, [pos] + ret[1]
    map[pos[0]][pos[1]] = 0
    return False, []

def getPath(map: List[List[int]]) -> str:
    copied_map = [i[:] for i in map]
    # print(copied_map)
    have_sol, sol = dfs(copied_map, (1, 0))
    if not have_sol:
        return []
    return sol

def getAnswer(map: List[List[int]], path: List[Tuple[int, int]]) -> str:
    if path == []:
        return "来点fufu"
    ops = ''
    cur = path[0]
    for i in path[1:]:
        if i[0] == cur[0] + 1 and i[1] == cur[1]:
            map[cur[0]][cur[1]] = 's'
        if i[0] == cur[0] - 1 and i[1] == cur[1]:
            map[cur[0]][cur[1]] = 'w'
        if i[0] == cur[0] and i[1] == cur[1] + 1:
            map[cur[0]][cur[1]] = 'd'
        if i[0] == cur[0] and i[1] == cur[1] - 1:
            map[cur[0]][cur[1]] = 'a'
        cur = i

    now = (1, 0)
    while now != (height - 2, width - 1):
        op = map[now[0]][now[1]]
        ops += op

        # do op

        def walk(pos: Tuple[int, int], dire: Tuple[int, int], orth: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, int]:
            while True:
                next_pos = (pos[0] + dire[0], pos[1] + dire[1])
                if not walkable(map, next_pos):
                    break
                pos = next_pos
                spos = (pos[0] + orth[0][0], pos[1] + orth[0][1])
                dpos = (pos[0] + orth[1][0], pos[1] + orth[1][1])
                fpos = (pos[0] + dire[0], pos[1] + dire[1])

                wspos = walkable(map, spos)
                wdpos = walkable(map, dpos)
                wfpos = walkable(map, fpos)

                if wfpos and (wspos or wdpos):
                    break

                if not wfpos and wspos and wdpos:
                    break

                if not wfpos:
                    if wspos:
                        return walk(pos, orth[0], (dire, (-dire[0], -dire[1])))
                    if wdpos:
                        return walk(pos, orth[1], (dire, (-dire[0], -dire[1])))
            return pos

        dire = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if op == 's':
            now = walk(now, dire[2], (dire[0], dire[1]))
        if op == 'w':
            now = walk(now, dire[3], (dire[0], dire[1]))
        if op == 'a':
            now = walk(now, dire[1], (dire[2], dire[3]))
        if op == 'd':
            now = walk(now, dire[0], (dire[2], dire[3]))
    # print(map)
    return ops

def solve(img: Image) -> str:
    map = getMap(img)
    path = getPath(map)
    return getAnswer(map, path)

if __name__ == "__main__":
    img = Image.open(input("Filename: "))
    map = getMap(img)
    path = getPath(map)
    print(getAnswer(map, path))
