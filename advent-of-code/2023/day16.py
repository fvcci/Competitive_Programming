import sys
from icecream import ic
from collections import deque
from dataclasses import dataclass
from typing import Tuple
import re
from tqdm import tqdm
from math import gcd


def p2():
    deltas = {
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
        "^": (-1, 0),
    }

    visited = set()
    visited_special = set()
    def dfs(cur_dir, r, c):
        if not in_bounds(r, c) or (cur_dir, r, c) in visited_special:
            return
        visited.add((r, c))
        visited_special.add((cur_dir, r, c))

        match cur_dir+arr[r][c]:
            case ">." | "<." | "v." | "^." | ">-" | "<-" | "v|" | "^|":
                dr, dc = deltas[cur_dir]
                dfs(cur_dir, r+dr, c+dc)
            case ">|" | "<|":
                dr, dc = deltas["^"]
                dfs("^", r+dr, c+dc)
                dr, dc = deltas["v"]
                dfs("v", r+dr, c+dc)
            case ">/" | "<\\":
                dr, dc = deltas["^"]
                dfs("^", r+dr, c+dc)
            case "</" | ">\\":
                dr, dc = deltas["v"]
                dfs("v", r+dr, c+dc)
            case "v-" | "^-":
                dr, dc = deltas["<"]
                dfs("<", r+dr, c+dc)
                dr, dc = deltas[">"]
                dfs(">", r+dr, c+dc)
            case "^/" | "v\\":
                dr, dc = deltas[">"]
                dfs(">", r+dr, c+dc)
            case "v/" | "^\\":
                dr, dc = deltas["<"]
                dfs("<", r+dr, c+dc)
            case _:
                assert False

    ans = 0
    for i in range(len(arr)):
        visited = set()
        visited_special = set()
        dfs(">", i, 0)
        ans = max(ans, len(visited))
    for i in range(len(arr)):
        visited = set()
        visited_special = set()
        dfs("<", i, len(arr)-1)
        ans = max(ans, len(visited))
    for i in range(len(arr[0])):
        visited = set()
        visited_special = set()
        dfs("v", 0, i)
        ans = max(ans, len(visited))
    for i in range(len(arr[0])):
        visited = set()
        visited_special = set()
        dfs("^", len(arr[0])-1, i)
        ans = max(ans, len(visited))

    ic(ans)


def in_bounds(x, y):
    return 0<=x<len(arr) and 0<=y<len(arr[x])


def p1():
    visited = [["."]*len(arr[0]) for _ in range(len(arr))]
    deltas = {
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
        "^": (-1, 0),
    }

    visited_special = set()
    def dfs(cur_dir, r, c):
        if not in_bounds(r, c) or (cur_dir, r, c) in visited_special:
            return
        visited[r][c] = "t" if arr[r][c]=="." else "s"
        visited_special.add((cur_dir, r, c))

        match cur_dir+arr[r][c]:
            case ">." | "<." | "v." | "^." | ">-" | "<-" | "v|" | "^|":
                dr, dc = deltas[cur_dir]
                dfs(cur_dir, r+dr, c+dc)
            case ">|" | "<|":
                dr, dc = deltas["^"]
                dfs("^", r+dr, c+dc)
                dr, dc = deltas["v"]
                dfs("v", r+dr, c+dc)
            case ">/" | "<\\":
                dr, dc = deltas["^"]
                dfs("^", r+dr, c+dc)
            case "</" | ">\\":
                dr, dc = deltas["v"]
                dfs("v", r+dr, c+dc)
            case "v-" | "^-":
                dr, dc = deltas["<"]
                dfs("<", r+dr, c+dc)
                dr, dc = deltas[">"]
                dfs(">", r+dr, c+dc)
            case "^/" | "v\\":
                dr, dc = deltas[">"]
                dfs(">", r+dr, c+dc)
            case "v/" | "^\\":
                dr, dc = deltas["<"]
                dfs("<", r+dr, c+dc)
            case _:
                assert False
    dfs(">", 0, 0)

    ic(sum(list(map(lambda x: x.count("t") + x.count("s"), visited))))


def main():
    assert len(sys.argv) == 3
    sys.setrecursionlimit(5000)
    TEST_INPUT_STATE = sys.argv[2]
    TEST_STATE = sys.argv[1]

    if TEST_INPUT_STATE == "test":
        inps = tests
    if TEST_INPUT_STATE == "prod":
        inps = prod

    global arr
    for inp in inps:
        arr = [s.strip() for s in inp.split("\n")[1:-1]]
        if TEST_STATE == "p1":
            p1()
        elif TEST_STATE == "p2":
            p2()


tests = [
"""
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
""",
]


prod = [
"""
\\.......\\..//-.............-/....|....../-....|..................................|........--/.................
..|/..-..\\..........\\.....|......\\...-....../...................................................|.../||\\......
....././\\..........-|....|....-..........................\\.......|.............................-/\\............
...........\\..-...\\...................|.......\\/./../...|.....-.|....|.........................|..............
............|-..............-....................-...\\.........|.............-..................\\...|.....//..
.....\\......................./............|..................|...|.............................../...........|
.........-..-...|...\\....-........................../....-.........-|.......|......|....................-.....
............../..../...../..\\..../................../............../..\\.................././......./..........
...-..|.....-./\\...../..../.|..\\.......-........................../.\\.............\\...........................
............|.-..../.............................|......\\.........|......--....-.........-..................|.
..|..\\........../...\\\\............\\........\\-...........-....|.....\\....|..................|../...../.........
....|..-....................-./-...............................|......./........../....|.....\\.|..\\...\\.......
..../......................|.....|...............-..../\\......................-.......\\.......................
............................\\.|.-.|.............-.................................................-...........
...|.-.......................\\|..-......-.................|.......-..\\.......\\-..................|............
.............................\\......................\\.../.\\.|...........\\....|..\\.............................
-.../...|................/.-......./..........|.........|........./||.-.........\\.....\\...-............./.|...
........../......../-.........................................../.......-|.|....................|...|../...../
......|................|............./.......\\.............-..............\\|.......-..\\./...../.-.../....../..
/............|\\........../.......\\......-..|......../-../.........|\\....../............\\.........|...|........
...............-.........|........................../.........\\............-\\....\\......../..................|
................\\.\\................\\....-.......-.....-......|..|...\\/........./...../..|.............|.......
............................................................................................................/.
................................|..-/...................../.....-.............|...-...........................
...................-/..................||./.............|..........|..................-.../..................|
..................\\/...|...\\.-.........../....-......................-\\.......|......./.........|..|.\\..-.....
........................|.-..................-........................./................\\.../...\\...|.........
..................-.........-/.....\\......|...../\\...-......\\....-....................................../.....
.....................|..............\\........\\....\\...............-........../......\\...........\\.............
...\\./......................-.\\..........\\.-..\\........-.................-.......-.||......................./.
...|..............\\..|............\\....|............|.....\\......../...........-...................\\...../../.
.........\\.........................\\.............../........//.................|.........\\.-...............-..
.............\\....-..../..-................./...|/...-...................|../.../.............-......../.....|
-.....||/.......\\......../..............................|...............................................-.....
.......|......\\........../|........................../-........../.\\..\\..............-.......|/|....-.........
../-.............-.\\-........./........-........\\...|...........-.\\./..\\.\\....................................
/.\\................../.....|...........-............-.......-......./.\\.\\..|...........\\......../.............
..............................|.....-...|...\\.......-.........\\..\\-..........-....\\......|...........|/...-...
.......\\......\\\\......-.....-.....-........|../........\\..|.............\\../................../...\\......./..\\
..-.........|............./............./.-.|.....|...../..............................................\\...|..
|......................./......-....-............/.................//...........\\.............-..\\............
............\\.....................-......-..|.\\.......\\/..........\\............/....\\.../.....................
|.............................|........./........................\\.................../.........|........../\\..
.../...|/.-.......-.............\\......................................./........--..................\\........
.\\...........\\..-|............-...-.\\...../...........-..|.............././.................|........../......
...............-......................./..............\\..\\........................\\.............-../..........
................................\\..../..................\\.....................\\............/............./....
...-..../../.......-............-......|...../.........|............................|...../../..............-|
.........|.......-..../..........................................\\|.|./.....-..\\.-.....................|......
............\\............................................|................-...-................\\..............
|...................................-...|/......|............./........./...|...................|....\\........
|......\\-......................./.-.............../.|\\-..|................-.....|../-\\.|.-..-|.........-.|-\\.-
......-......|-......|.................-.-..\\..../-./.............................................|-......./..
.-...............................\\...........................-|.......-.......................................
.............\\.|....|....\\.............../..\\..|..................../.............|...-\\......................
........-.\\/.....................|........-......./............../..............\\..\\.............|......./....
..-....../-..........................|...../..\\...............\\..........-....\\...........|.\\...\\.............
...........|............................................../...................\\.\\.\\...........................
../.................|\\.|.\\..-..\\........\\...-..-........-..\\....-...............-..............\\...........|/.
........\\.|....................../...........//................/.................\\..../.....-.................
.....\\...\\.....\\.......\\......\\.....-|./..|............./|./|-\\.........................-........--...........
..|................../.....\\.....|.......-...|............-../................-...\\........-.......|..\\\\......
.....|......../....\\....../...\\........................................\\..\\..............-..................|.
....//......\\.........-......./.\\..\\........./..........-....-.....\\..-...|...................\\.../......|....
...............|...................../.\\.............-...\\.....\\..|..................../.............\\.....|..
\\.....................-............/.............\\...-...................../...-..-.....|./..............\\....
........................-../......\\.............-........-.\\/.....|.-..........-............../..-....-\\\\..-..
.........../.................\\.....|..../.\\.........|........./...-..........................\\................
|....................../..../.......................-................\\...................................-./..
...|.......\\-.......\\........\\..........-........................./...../.........................-../........
.............\\.......-....-..|...\\..../.-...\\......|....................|..-./...................\\............
...............\\./.\\...............|.............\\./......|...........................-.........../.|.........
...../....../..............|.................../.....|.....\\............................/.\\...../...\\|........
.\\............/......................-......./................-/./.|....................................-.....
.................../.......\\........../-.............................|\\.......................................
../....................\\....../......./.....................................|................-/\\...|..........
\\................/........................--.........../\\....\\../....../..........|-............-.............
./\\..................--......\\..../.....\\.......-..............................|.............-.............\\..
....|.....|...............................\\//.................|..........|.-.........\\................././....
../....-...............-...|...............-...-................./......-..-/...........-....../..........|-..
..........|.|/..............................-./|...|..|......\\............................-...-...|...........
..\\..........................................................-......................../../................-...
.....|\\..........................\\................|................\\.../.......\\..|.\\.........-.......\\.-.....
.......................|..\\..........|.......\\.-.................\\\\........-............|.....................
......./.................|.\\...|............................./\\............\\.....|.....|-...|.....|.......|...
....../...-.........../|...............-.............................\\../...........\\...........|...........|.
..-..................\\....\\/.........|.....\\......................-...........................................
....|.....-................................/.........-|...........\\....\\.-./....\\........................../..
....../........\\................|......\\.......|.................................\\............................
....-......./......./-.../.......\\...........|..............|................................|......|.........
-....................-.............................|......\\......|.........//...........\\........\\............
\\............./...../.....-.......-\\...........-...........\\.|.............-/.....|......|.../................
.......................|/\\..\\............|..|...................../.......-\\........|.....|....\\.....\\...-....
.......-............|........................../..\\.|.................\\...............\\............|...|...|..
......................../..-.......-.......-...-.............\\............-......--..\\..................|...\\.
...............|.|......|.....\\................-.........../.........\\............\\.............-.............
..\\..........................|./......-........|....-.............-.......-.....\\................/............
...../..................................................|......\\..-........|..|.....................\\.....-...
.....\\....|.........|.........|.................../.............\\......|.......|..........\\............./.../.
./.../............../.|....\\./..././...................\\...........|...........-......................\\....\\..
.../..............................-...............................\\.............../..........-.............../
|..\\-.........\\../...........|.\\..........-.........../..........|-...................................-.......
...........................|../.....\\.........................|.....\\........../..............................
..................-..........|.........|....|............../...-..../.............../-........\\\\.\\.......-....
.............---..../....................-....-......../....../.........\\..\\............................../...
|.....|.......................././...............|.../..|.\\............-.................../............./....
..-........\\............./../|..........................--....|..\\.........|/./................/...../........
..........\\|.....................................--............/....../............\\.|......|.......-|......\\.
..........|-........\\....|.....................\\................................-\\...|......../.........\\..|..
..\\\\.........\\..|../................|.........\\.....--...-...\\................/.............................\\.
"""
]


if __name__ == "__main__":
    main()
