import sys
from icecream import ic
from collections import deque
from dataclasses import dataclass
from typing import Tuple
import re
from tqdm import tqdm
from math import gcd


def p2():
    start = None
    for r in range(len(arr)):
        for c in range(len(arr[r])):
            if arr[r][c]=="S":
                start = (r, c)

    assert start != None

    vis2 = [[False for x in range(len(arr[_]))] for _ in range(len(arr))]
    vis2[start[0]][start[1]] = True
    q = deque([start])

    while len(q)!=0:
        cr, cc = q.popleft()
        a = arr[cr][cc]
        dirs = []
        match a:
            case "F":
                dirs = [(1, 0), (0, 1)]
            case "J":
                dirs = [(-1, 0), (0, -1)]
            case "L":
                dirs = [(-1, 0), (0, 1)]
            case "7":
                dirs = [(1, 0), (0, -1)]
            case "-":
                dirs = [(0, -1), (0, 1)]
            case "|":
                dirs = [(-1, 0), (1, 0)]
            case "S":
                dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            case ".":
                assert False

        for dr, dc in dirs:
            nr, nc = cr+dr, cc+dc
            if not (not vis2[nr][nc] and 0<=nr<len(arr) and 0<=nc<len(arr[nr])):
                continue
            valid_dst = {}
            match (dr, dc):
                case (-1, 0):
                    valid_dst = {"|", "F", "7"}
                case (1, 0):
                    valid_dst = {"J", "L", "|"}
                case (0, 1):
                    valid_dst = {"-", "J", "7"}
                case (0, -1):
                    valid_dst = {"-", "F", "L"}
                case _:
                    assert False

            if arr[nr][nc] not in valid_dst:
                continue

            vis2[nr][nc] = True
            q.append((nr, nc))

    id = 0
    vis = set()
    ids = [[-1 for x in range(len(arr[_]))] for _ in range(len(arr))]
    for r in range(len(arr)):
        for c in range(len(arr[r])):
            if ids[r][c] != -1 or ids[r][c] in vis or vis2[r][c]:
                continue

            # find a path to the border
            ids[r][c] = id
            q = deque([(r, c)])
            flag = False
            while len(q)!=0:
                cr, cc = q.popleft()
                a = arr[cr][cc]
                # assert a == ".", str(a)
                assert -1 not in vis

                for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                    nr, nc = cr+dr, cc+dc
                    if not (0<=nr<len(arr) and 0<=nc<len(arr[nr])):
                        vis.add(id)
                        flag = True
                        break
                    if vis2[nr][nc]:
                        continue
                    if ids[nr][nc] != -1:
                        if ids[nr][nc] in vis:
                            vis.add(id)
                        flag = True
                        break

                    ids[nr][nc] = id
                    q.append((nr, nc))

                if flag:
                    break

            id += 1

    og = [a.copy() for a in ids]
    for r in range(len(ids)):
        for c in range(len(ids[r])):
            if ids[r][c] in vis:
                og[r][c] = "O"
            elif ids[r][c] != -1:
                og[r][c] = "I"

    for r in range(len(ids)):
        for c in range(len(ids[r])):
            if og[r][c] != "I":
                continue
            # go right
            pairity = 0
            seen_hori = ""
            seen_s = False
            for nc in range(c+1, len(arr[r])):
                if not vis2[r][nc]:
                    continue
                match arr[r][nc]:
                    case "|":
                        pairity += 1
                    case "F":
                        assert seen_hori == ""
                        seen_hori = "F"
                    case "L":
                        assert seen_hori == ""
                        seen_hori = "L"
                    case "7":
                        if seen_hori == "F":
                            pairity += 2
                        elif seen_hori == "L":
                            pairity += 1
                        seen_hori = ""
                    case "J":
                        if seen_hori == "F":
                            pairity += 1
                        elif seen_hori == "L":
                            pairity += 2
                        seen_hori = ""
                    case "S":
                        seen_s = True
                        break
            # skip line with S (since idk what to do with it) and go left
            if seen_s:
                pairity = 0
                seen_hori = ""
                for nc in range(c-1, -1, -1):
                    if not vis2[r][nc]:
                        continue
                    match arr[r][nc]:
                        case "|":
                            pairity += 1
                        case "J":
                            assert seen_hori == ""
                            seen_hori = "J"
                        case "7":
                            assert seen_hori == ""
                            seen_hori = "7"
                        case "F":
                            if seen_hori == "7":
                                pairity += 2
                            elif seen_hori == "J":
                                pairity += 1
                            seen_hori = ""
                        case "L":
                            if seen_hori == "7":
                                pairity += 1
                            elif seen_hori == "J":
                                pairity += 2
                            seen_hori = ""
                        case "S":
                            assert False

            if pairity % 2 == 0:
                og[r][c] = "O"

    ic(sum(list(map(lambda x: x.count("I"), og))))

    # entrances = [
    #     ########## IMPOSSIBLE OUTCOMES
    #     # |F- ||-
    #     # |x  |x
    #     ########## TOPLEFT
    #     # 7L-
    #     # |x
    #     (-1, 0, "L", -1, -1),
    #     ######## TOP RIGHT
    #     # -JL
    #     #  x|
    #     (-1, 0, "J", -1, 1),
    #     ######## RIGHT TOP
    #     # --L
    #     #  xF
    #     (0, 1, "F", -1, 1),
    #     ######## RIGHT BOTTOM
    #     #  xL
    #     # ---
    #     (0, 1, "L", 1, 1),
    #     ######## BOTTOM RIGHT
    #     #  x|
    #     # -7L
    #     (1, 0, "7", 1, 1),
    #     ######## BOTTOM LEFT
    #     # |x
    #     # 7F
    #     (1, 0, "F", 1, -1),
    #     ######## LEFT BOTTOM
    #     # Jx
    #     # --
    #     (1, 0, "J", 1, -1),
    #     ######## LEFT TOP
    #     # J-
    #     # 7x
    #     (0, -1, "7", -1, -1),
    # ]

    # # Verify all the I's
    # for r in range(len(ids)):
    #     for c in range(len(ids[r])):
    #         id = ids[r][c]
    #         if og[r][c] != "I":
    #             continue
    #         for ar, ac, val, br, bc in entrances:
    #             if arr[ar][ac] != val:
    #                 continue
    #             q = deque([(ar, ac)])
    #             flag = False

    #             while len(q)!=0:
    #                 xr, xc = q.popleft()
    #                 a = arr[xr][xc]
    #                 dirs = []
    #                 match a:
    #                     case "-":
    #                         dirs = [(0, -1), (0, 1)]
    #                     case "|":
    #                         dirs = [(-1, 0), (1, 0)]
    #                     case "S":
    #                         dirs = []
    #                     case ".":
    #                         assert False
    #                     case _:
    #                         dirs = [(0, -1, (0, 1), (-1, 0), (1, 0))]

    #                 for dr, dc in dirs:
    #                     nxr, nxc = xr+dr, xr+dc
    #                     if not (0<=nxr<len(arr) and 0<=nxc<len(arr[nxr])):
    #                         vis.add(id)
    #                         flag = True
    #                         break
    #                     if ids[nxr][nxc] != -1:
    #                         if ids[nxr][nxc] in vis:
    #                             vis.add(id)
    #                         flag = True
    #                         break

    #                     ids[nxr][nxc] = id
    #                     q.append((nxr, nxc))

    #             if flag:
    #                 break


def p1():
    start = None
    for r in range(len(arr)):
        for c in range(len(arr[r])):
            if arr[r][c]=="S":
                start = (r, c)

    assert start != None

    dis = [[0 for x in range(len(arr[_]))] for _ in range(len(arr))]
    vis = set([start])
    q = deque([start])

    while len(q)!=0:
        cr, cc = q.popleft()
        a = arr[cr][cc]
        dirs = []
        match a:
            case "F":
                dirs = [(1, 0), (0, 1)]
            case "J":
                dirs = [(-1, 0), (0, -1)]
            case "L":
                dirs = [(-1, 0), (0, 1)]
            case "7":
                dirs = [(1, 0), (0, -1)]
            case "-":
                dirs = [(0, -1), (0, 1)]
            case "|":
                dirs = [(-1, 0), (1, 0)]
            case "S":
                dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            case ".":
                assert False

        for dr, dc in dirs:
            nr, nc = cr+dr, cc+dc
            if not ((nr, nc) not in vis and 0<=nr<len(arr) and 0<=nc<len(arr[nr])):
                continue
            valid_dst = {}
            match (dr, dc):
                case (-1, 0):
                    valid_dst = {"|", "F", "7"}
                case (1, 0):
                    valid_dst = {"J", "L", "|"}
                case (0, 1):
                    valid_dst = {"-", "J", "7"}
                case (0, -1):
                    valid_dst = {"-", "F", "L"}
                case _:
                    assert False

            if arr[nr][nc] not in valid_dst:
                continue

            dis[nr][nc] = dis[cr][cc] + 1
            vis.add((nr, nc))
            q.append((nr, nc))

    ic(max(list(map(max, dis))))


def main():
    assert len(sys.argv) == 3
    TEST_INPUT_STATE = sys.argv[2]
    TEST_STATE = sys.argv[1]

    if TEST_INPUT_STATE == "test":
        inps = [test, test2, test3, test4, test5, test6]
    if TEST_INPUT_STATE == "prod":
        inps = [prod]

    global arr
    for inp in inps:
        arr = [s.strip() for s in inp.split("\n")[1:-1]]
        if TEST_STATE == "p1":
            p1()
        elif TEST_STATE == "p2":
            p2()


test = """
.....
.S-7.
.|.|.
.L-J.
.....
"""

test2 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""


test3 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

test4 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""

test5 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

test6 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

prod = """
F-L----F7-7.F-7JJ.F--L-.F|F77.L|7.FLF-7.JJ--7FF-F-F7F7.7-F-7.L.FL7F|7--777.FJ-|7J-F-J-77-FF-F-7.JF77.L.JFL.L-|-FF7-77FL--F77.7-|77F7|7FF7-7-
J|F7.LL|.F7.FL|J-77--JJ7L|-|-F-7L7-|LJ|F|JL|L-JJ|L|--7FF77.|-L7|LFLF-7FL--LL.FLJL-JFF-F7.-LJLF|J-LJ|FJ.|7-7L-JF|.J.LF7|L7.LF-|7F7-|-7-J7|7.|
FF7J.7L|-7|FF7|L7|L|.LF7-JFLJJ.J7JJFJ-7.L-LLJJ|LJ7LL|.JLL---.LFJ7L-LJL-|JJ-|-F.LJ7|FLF-J.L7.FJ||F||L|L7--F..FLF7-L7|LLJ7L7.-7||||J|FJ.LLJ7F-
FJ.LF-7-FJLJ-|7-7J777..|-FJ7.FJ.|.F|LFL-L7L|..--L|7.F-7-L|..FF|JF|7J.|7|FF-|.LF7LL77.J.LJL|7LF-77.|FFJ|7FLJF|-F7..FJF7L7.FJF7LJ||--|JJLLJF.J
|FF7LFL7LJJL|.|.||L77--|7F---L.F|77JFL7.F|7FL7.F7LJ-7-JJLJ.--JLJFJ77F|7F|-.|L-LJ7-LJ7FJ7.|J|-F-J|FL7|-L-J7|-.L7JJ-L||L-|7J.LF7FLL-|||.FF-7J.
FFJ-7LL7JF-.LL|-L--||.F|FL7J..LLJ|J.J.FF7L||JFJLL.J-J7LF7J77.7.||.F-FJ-|J.77.F-LLJJ|L-7|L---7JFL-7FJ-7FFL|7FLFJ|L|F-JL|.|.|-J7-LL-FL-.FFLJJ7
LL7.L--|7LJ7J.7|FL7.F77FF..-|7-L-|F7.L7JLFJ|LL|.LF-FLL7LLL-|7|F7F-7-J.FL-F|-J77-|.F-.L-J.L|||F|JLJJ7FJF7|J|7FL77FL|.|L|J7FF-L--..L|.F-77JL7-
|LF-7L.|FLLJ.LJ7-7FJL--FJ7L.7J.|JL|J-7|F7-.J7L|L-L77J|L7..FJF7LF77|J-.L--.-7L-F7F-J.F-|J|.FL7-7-F|JF.FL|---J-FFJF|.F|7F-FF.FL7--..J.|LL---JJ
|.--7.F|F7.J-LLJJLFJ.|.|-||-|LF77-7|FF||||7.JFFJF-J7|.F7FFF7||FJ|7|.|.|.L-FJFLJL|7|F|.L7.L|L|.-.LJF|F7|..FFJ-LJF.JJ7L||LLJ7---JLL-|7LFF7-7.|
F-LJJF-FJ-|..||L.JJ|-77|LF-F77F-7|LF7-L--7-|.FJ-JJ-JFF|L--J||LJFJJ-F-FJ.|FJFJJ..L7.|.F7J--L.|7.JJ.--7L7JF7L|J|FF7.LF7LJ-|||.|L-JL7-7-FJ-FJ-7
FJ||FF7-J|L|-LF7LF7J7F7F7|FJ|FJFJJ--J|L|7LL|7LL-77J7FFL7F-7LJF7L7J.7-|.-F7|||-F|-FFF-J|J.F|7F-7.|FL-J-LJ-|7LFF7||7-|L7-F77-LJ|.FFLJL-|L|L|..
J.LJ-|LL-77F7.||-J|F-JL|L7L7|L7|.|-|FF-F..LJ|.LL|-F7-F7LJFJF7|L-JLFF.L-|JF7F7F7JJF7L7FJF7JLF|FJ777.|.7.|F77-FJLJ|F7L7|.||..JJFLJ77F7|F-J.|-7
|77JFL77L|-J|--|7F-||LFL7|F||-|L77--F7J|7L.F-|J|LFJ|||L7JL7||L7F7F7J|..L||LJL-7F-JL7|L7||7-FJL-777.F.F-7||F7L7F-J|||||FJL777FL-L---.JJ|LJ.L|
7JL--7.|.|77L7.F7-FF7FF-JL7||-L7|F7.||.77L|--7FF7L7L7|FJ77LJ|FJ|LJ|7|FF7-L-7F-JL--7||FJ||F7|F--JF--77L7LJ||L7|L7FJL-J||F-J||J.77F|.|-|7FL.FF
.F7F7F7JF.F--7-L7.F||7L--7LJL--J|||-||FF7F7JFF7||.L7||L-77F-JL-JF7|F7FJ|7|FJ|F7F--JLJL7||||||F7||F-JF7|F-JL7|L7||F---J||||7|-J-L-|7L7F-|77F-
FL||-L7F|7JL7J77F7FJL7F-7L-7F---J|L7||FJ|||7FJ|||7-|||F7L7L-7F-7|LJ||L7L-7L7|||L--7F--J||||||||-|L-7|||L-7.||FJ||L--7FJL-7L7LL|J.|J-LJ||LJJ.
|JLF-.LL|-J|L7FF||L7FJ|FJJFJL7FF7|FJ||L7||L7L7||L-7||||L-J|FJL7LJ|L|L7|F-J|||||F7.|L7F7|||LJLJL7L7FJ||L7FJFJ|L7LJF--J|F--J7J..F7FL.|-LFFJ|F7
.|7||.L|J.FL7FF-JL7|L7||F7L7FJFJ|||F||.|||FJFJ|L-7||||L7F7FJF7L-7F7L7LJ|F7FJLJ|||FJFJ||||L-7F--JFJL7|L7|L7L7|FL7FJ-F7||-LF7JFFJL7LJ77F7-.||7
L7FFL7-|-J--7-L--7|L7||||L-J|FJFJ|L7||FJLJL7L7L7FJLJ||FJ||L7|L7FJ|||L-7|||L--7|||L7|FJ|||F7||F-7L-7LJFJ|FJFJL-7||F7|||L-7||77L7JJL|-FJJ-77JL
L7LLJJ.JFLL7JFF--JL7|LJ|L--7||FJFJFJ||L7F--J|L7|L--7|||FJ|FJL7||FJ|F7-||||FF-J|||L||L7||||||||FJ|FJF-JFJL7L--7LJLJLJLJF-J||LFFJ.7JL.|L|.|F.|
F|.|--F7|-FJ7L|F--7LJF-J.F7|LJL7L7|FJL-J|F7FF7||7F-J|||L7LJF-JLJL7||L7|LJL7L-7LJL-JL-J|||||||||F7L7L-7|F7L7F7|F------7L--JL-7|--7F|FJ.|FJ|7.
7F-7-JLJLF-7LLLJF-JF7L7-FJ|L7F-JFJLJF---J|L7|||L7L-7LJL7|F7L7-F--J|L7||F--JJ|L----7F--J|||||LJLJ|LL7FJLJL7||||L77F7F7L------JJ7LL777|-F7||7F
|FJJ..LL-7|||FF7L-7|L7L7L7|||L-7L7F7|7F7.L7||LJFJF7|F--JLJL7L7L--7|FJ||L7F-77F7.F7|L-7FJLJLJF---JF7||F7F-J|||L7|FJLJL7F7F-7||-F7L--77LJLJJ7|
LL.F-|7JJ.J-FFJL-7LJFL7|FJ|FJF-J.|||L7|L7FJ||F-JFJLJL7F7F7F|FJF7FJ|L7LJFJL7|FJL7|||F-JL---7FJ-F7-||||||L-7|||FJLJF--7LJLJFJF7FJL77FLL-JLL7|L
|FJ|LJ|L-F-LFL7F7L-7F7||L7||FJJF7LJL7||FJL7||L-7L--7FJ||||FJL7|||FJL|F-JF-J|L-7LJ||L7F7F7|||F7|L7|||LJ|F7|||||F--JF7L----JFJ||F-J-|7JJ|-|JJJ
JJ-J-JJF-7|L|-LJ|F7LJLJL-JLJ|F7|L7F7|LJ|F-J||F-JF7F||.|||||F-J||||F-JL-7L-7L-7L7FJ|FJ|LJ|FJ||||FJ||L7FJ|||||S|L---J|F7F7F7|FJ||F7JJF-L|-|L77
JLF-7..|7||F|JF-J||F7F7F-7F7LJ|L7||||F-JL-7|||F7||FJ|FJ||LJ|F7||||L7F-7|F7|F7|FJ|FJL7L-7LJFJ|||L7|L-J|FJ||||LJF----J|||LJ||L7||||FF777|F7FFJ
FL|F7-|FJ-L-L.L--JLJ||LJ|LJL7FJFJ||LJL7JF7|LJ|||||L7||FJL-7|||||||FJL7LJ||LJ||L7|L7FJF7L-7|FJLJFJL--7|L7||||F-J7F--7|||F-JL7||LJ|FJ|.|7JL-JJ
|.-|J.L-J|FJ|7|LF--7LJF-----JL7L7|L-7FJFJ|L-7||||L-JLJL-7FJLJLJLJLJF-JF7|L7FJL7||FJL7||FFJ|L-7FJF7LFJL7||||||F--JF-J|||L7F7|LJF-J|FJF77J||..
F-LL--.FL-7.|J-FL-7L--JF-----7L-J|F-JL7|FJF-J|||L--7F---JL--7F----7|F7||L7|L-7|||L-7LJL7L7|F7|L7||FJF7||||||||F--JF7||L7LJ||F7L7FJ|FJL7.J7FF
777F7F-J-|.LF7--JFJF7F-JLF--7L-7FJL-7FJ|L7L7FJ||-F-JL7LF7F7JLJF7JFJLJ||L7||F7|LJL-7L--7L7||||L7LJLJFJLJ|||LJLJ|F7-||||FJF-J||L-JL7||F-J7FLJ.
J--L7F.J.7FL||FFFL7|||F-7L-7L--JL--7|L7|FJFJ|FJL7L--7L7|LJ|F7FJL7L7F-JL7LJ|||L-7F-JF-7L7||LJ|LL7F--J||FJLJF7F-J|L7||||L7L--J|F--7|LJL--77.L7
F--LLLL7LL7LF7F7F7LJLJL7L-7L----7F-J|FJ||FJFJ|F-JF7-L7|L7FJ|||F-JFJ|F-7L7FJ||F7||F7L7||||L-7|F7||F7F7FJF--JLJ-FJFJ||||FJF---JL7FJ|F-7F7L-77J
J|-7.|J|FJ-FJLJ|||F--7LL-7L-----JL--JL7|LJFJ7|L-7||F7||FJL7|||L7FJFJL7L7||FJ|||||||FJ|FJL7FJ||LJ||||LJFJLF-7F7L7|L|LJLJFJF--7FJL-J|-LJ|F-J77
LL-F-JF|L.FL-7FJ||L7FJF7FJF--7F7F--7F-JL7FJF7L7FJ||||||L7FJ|||FJ|FJF7L7|||L7|||||||L7||F-JL7|L7FJ|||F-JF7|FJ||J||FJF7F7L-JF7LJF7F7L--7LJFJLJ
7JLJL-FJJ|7F7||FJ|FJ|FJ|L-JF-J|LJF7||F-7|L7|L7|L-J|||||FJ|FJLJ|FJL7|L7|||L7|||LJ||L7|||L7F7|L7|L-J|||F7|LJL-JL7|LJFJLJL-7FJL7FJ|||F-7L777-J.
|..L7LJ.LF-JLJ|L7|L7|L7|F7FL--J-FJLJLJ7||FJL7|L--7LJ||LJJ||F--JL-7|L7LJ|L7|||L7FJ|FJ|LJL||LJFJ|F--J|||||F-----J|F-JF7FF7|L-7LJFLJ|L7L7L77-7J
7.77||.F||F7F7L-J|FJL7||||F7F--7L-----7||L7FJ|F-7|F7|L--7||L7F7F7|L7|F-JFJ||L7|L7|L7L-7FJ|.FJFJL7F7|||LJL7F--7FJL-7||FJ||F7L----7|FJ-L7|JFF.
|..FF7.F-LJLJL--7LJF-J||||||L-7|F7F---JLJFJ|FJ|.LJ|LJF7FJLJJLJ|||L7||L-7L7||-LJ|||FJF7|L7L7|FJF-J||||L7F7LJF7LJF-7LJLJFJ||L-7F7FJLJ|FFLJFJ..
|.F7L|-J-|LF----JF7L-7||||||F7||||L-----7L-JL7L-7-L7FJ|L---7F-J|L7||L7FJFJ|L-7F-J|L7|||FJFJ||.|F7|||L-J||F-J|F7L7|F-7FJ|LJF7LJLJJLL7F-7LJ-FJ
JJ.|7L7LFJ-L-----JL-7||||LJ||||LJL---7F7|F---JF-JF7|L7|F7F7|L-7|FJ|L-J|FJFJF7||F7L7||||L7|-LJFJ|LJ||F--JLJF7LJ|FJ||-LJF7F7|L--7F7-7L7J-7L.7.
||F||-J7LL7|JF------JLJLJF7LJLJF7F--7LJLJ|F7F7|F-JLJFJ||||LJF-J|L7L-7JLJ.L7|||||L7|||||FJL--7L-JF-J|L-----JL-7||7|L---JLJLJF--J||.L7|JF|FF-J
.-J-F.L|7FJ-FL-7F--7F---7|L-7F-JLJF-JF7F7LJ||||L7F-7|L|||L-7L-7|L|F7L--7F7||||||FJ|||||L7F7FJF-7L-7|F------7FJ|L7L---------JF7FJL7|LLJF.JJ|.
FLL7|FFL77JJF-7LJF-J|F--J|F7||F--7L-7|LJ|F7LJLJLLJFJL7LJL7FJ|FJ|FJ||F-7LJ|||||||L7|||||FJ||L7L7L--J|L7F7F7-LJ|L-JF-7F7F-----J||F-J7.|.|.|..F
FJ|L--J7LFJ-L7|F7L--JL-7FJ|LJ|L-7L--JL-7LJL7F-77F7|F-JF7J||7FJFJ|FJ|L7|F-J||||||FJ||||||FJL7|-L---7|FJ|LJL-7|F7F7|FJ|LJF-----J|L---7FL7F-F7|
|-JJJ7|7F|FF-JLJL------JL7L7FJF7L---7F7|F--J|FJFJLJL--J|FJL7L7|J|||L7||L-7||LJLJL-JLJ||||7JLJF7F-7LJ|FJF7F7L-JLJLJL-JF-J.F7F7.|F---J7.LJ7|FL
L7|.LLL7-||L7F7F---------J.LJFJL--7FJ||||F7FJL7L7F-7F7FJL7FJ|LJFJL7FJ||F7||L--7F--7F-J||L7F--JLJFJF7||FJLJL7F7F7F-7F7L---JLJL-JL--7|F77|--.J
.FJF7JLJ.FF-J||L7F-7F7F7F7F7FJF--7|L-JLJLJLJF7L7|L7||||F-JL---7|F7|L7|LJLJ|F--JL-7LJF7||FJL-7F-7|FJ|LJL---7LJLJLJL||L7F--7F7F-7F7FJFJL7|J|7.
|J-L-77.F|L-7||FJL7|||||||||L-J|FJL-7F-7F7F7||FJL-JLJ|||F7F7F-J||||FJL-7F-J|F7LF-JF7|||LJF--J|-||L7||F----JF-----7||7|L-7||||J|||L-JF-J7F|FL
|.F7LJ|7L||LLJLJF-JLJLJLJLJL7LF7L--7|L7LJ|||||L-----7||LJ|||L-7LJ||L-7FJL-7LJL7L7FJ||LJF-JF--JFJ|FJL7L-----JF----JLJFJF7||||L7LJ|F-7L--7-L-.
.F7JJ---JL7|F---JF---------7|FJ|7F-JL-JF7LJLJ|F-7F--JLJF-J||F7|F-J|F-JL--7L7F-JFJ|FJL7FL7FJJF7L7|L-7L7F7F---J|F7F-7|L-JLJ||L7|F-JL7L7F7|J7--
LLJ-F7JL|FF-JF---JF--------JLJFJFJF7F7FJL7F-7|L7|L---7-L-7|||LJ|F7|L7F7F7L7|L-7L-JL7FJF7LJF-J|FJL--JFJ||L----7|||FJF7F--7LJ7LJ|F7FJFJ|LJLJ.L
J7|F-F--JFL--JFF-7L----------7|JL-JLJ|L7FJL7|L-JL----JF-7|||L-7||||FJ|||L7||F7|F---JL7||F-JF7LJF-7F7L-JL--7F-J|LJL-JLJF7L----7LJ|L7L-JJ-FJF.
LFF7JJ.F7FFF7F7L7L----------7||F-7.F7L-JL-7|L------7F7|FJLJ|F-JLJ||L7||L7||||LJL7F-7FJ||L--JL7FJFJ||F7F7F7LJF-JF------JL-7F--JJLL-JJL|-77-77
LL|JLF-F-7FJLJL-JF-----7F7F7LJ|L7L-JL----7LJF------J|LJL-7FJL-7F7LJFJ||FJ|||L7F-J|FJ|FJL7F7F7LJFJFJLJ||||L--JF7L-----7F-7|L---7-L7|.-.FLJLJJ
--777L7L7||F-7F--JF7JF7LJLJL-7|FJF-----7FL-7L---7F7||F-7FJL-7FJ|L7FJFJ||FJ||FJL--JL-J|F7LJ|||F7L-JF7JLJLJF---JL---7F7LJFJL-7F7|FL|7FJ7F|77|7
LLF-J|LFJLJ|FJL7F-JL7|L-7FF7||LJFJLF---JF77L-7F7LJL-JL7||F--JL7|FJL7|FJ|L7|LJF7F7F7F7LJL-7LJLJ|F7FJL-----JF------7LJ|F-JF7-LJLJ-7.|JF7J.L7||
F.|7FFJL---JL--JL7F-JL-7|FJL-JF7|F7L-77FJL--7||L--7F7FJLJL7F-7LJL-7||L7|FJ|F-JLJLJLJ|F--7|F7F7LJ|L--------JF7F7F7L-7|L--JL--7J-LJ7LLJ||-J.|7
777|7..FF---7F---JL7F--JLJF7F7||||L-7L-JF7F-JLJF77LJLJF7F7||7|F7F7|||FJ||FJL7F----7FJL-7|LJLJL-7|F--7-F----JLJLJL--J|F-----7|-F-LF7FLL-JF-JJ
L-|J-L-FL--7|L----7LJF--7FJ||||LJL-7L---JLJ|F7J|L-----JLJ|LJFJ|||LJ|||FJLJJ-LJF---J|F7FJL------JLJF7L-JF-------7F7F7|L----7LJ7|--.|-...--7.F
FLF.FLF7|F7|L7F7F-JF-JF-J||LJLJF---JF7F7F---JL-JF-7F-----JF-JFJ|L-7||LJJJ.LFJFJF--7LJLJF7F7F-7F7F7|L7F-JF---7F7LJLJ||F7F7FJF-7--FF|LF|77FF--
J|L-7-|L7||L7|||L--JF-JF7|F7-F7L----JLJLJF--7F7FJFJL--7F-7L-7L7|F7|||JJ|L7-F7L7|F-JF--7|||||FJ|||||FJ|F7L--7LJ|F---JLJLJ|L-JFJLF-F|7FJLFJ-J.
FFFL7-L7LJ|FJLJL--7FL--JLJ|L-JL---7F7F-7FJF-J||L7L---7LJFJFFJFJLJLJLJJF|7L-|L-J||F7|F-J|||LJL-JLJ||L7||L---JF-JL-----7F7L---J7-|L7L7L7LL.F-|
L-FF7|FL-7LJF-7F-7|F7F----JF-7F--7LJLJFJL7L-7||FJF--7|F-JF7L7|J7L|||JF-F-JLL7F7|LJ||L7FJ|L-7F----J|FJ|L7F7F7L-----7F7LJL7F-7.JJLLL-F--FL-7-|
.F7LL7F--JF7|FJ|FJLJLJF7F--JFJL7JL---7L--JF7LJ||FJF-JLJF-JL7||J|7.|.LL.J.F-FJ|||F-JL7||LL--JL--7F-J|FJ7LJLJL-----7LJL---J|FJ7-F77FFL7J|L7L-|
-|77|L|F7FJLJL7||F7F7FJLJF--JF-JF----JF7F7||F7LJ|FJ-F-7|F--JLJ.|J7L77L----J|FJLJL---J||F7F-7F-7LJF-J|F7F7F---7F-7L-7|F7F-JL7--FFJ---J.JF7FFJ
..L77L||||..F7LJLJ||||F--JF-7|F-JF----JLJLJLJL--JL--JFJ|L-----7.||F7J7|F|..LJJL7JF7F7LJ||L7LJFJF7L--J|LJLJF77LJ|L-7L-JLJF7FJFF|.F-J||-LL-7LF
|.JL-JLJLJF-JL----J|LJ|F7FJLLJL7FJF----7F7F7F7F-7F--7L7|F7F7F-JFF7|JLLJJ77.JL77FFJLJL--J|FL7FJFJL7FF7L----JL---7F7L7F---JLJ-LJ|F|7FJ-F-JLLJL
L-||-||F--JF7F-----JF7LJ|L7FF7FLJLL---7LJLJLJ|L7|L-7L-J||LJLJ-LFJ|J|.F|JLF7..L|JL7F-7F-7L--JL7L-7L7||F---------J|L7|L-----77L7|F777|JJ..FJ-J
L-JF-JFL7F7|LJF----7||F7|FJFJL--------JF7-F7-L-JL--JF--JL--7.F-|FJ.LFLJJ.|F7..|FFJ||||JL--7F7|F7L7|||L-----7F--7|FJL-----7L-7F7F777JJ.L-|JF7
.-.F7L|JLJLJF7L---7||||LJL7L-----------JL7|L---7F--7|F-----J-7-||LJFLJ-LLFLJ-F-7L-JFJ|F--7LJ|LJL-JLJL7F----J|F-J|L7F7F7F7L--J||||||J-F.JJF-F
FL7L-JF.|.|FJL-7F-JLJLJF--JFF------------J|F---JL-7|||F---7F-77||7JF7|7LL77.-L7|-|7L-JL-7|F-JF------7LJF-7F-JL7F|FJ|LJLJL7JF7|LJL-7F7|..FF7|
7FJ-J-JLJF7L7F7LJF-7F-7L7F--JF-7F7F---7F-7||F7LF7-|||||F--JL7|FJL7.||F7.7LJ-.F|L7F7F7F7F||L--JF-7F-7L--JFJ|F--JFJ|FJF--7FJFJ||F---J-7J7FFL77
|-7-|..|7|L-J||F7|FJ|FJFJL-7FJLLJLJF--J|FJ||||FJL7|LJLJL----JLJF7|.|LJ|7L7..7-L7||LJ|||FJL--7JL7LJFJJF-7L-JL-7||FJ|FJF7LJ|L7|||F-7..LFJ7-FJ7
7||F|.7LFL---JLJLJL7|L7|F-7LJF7F7F7L---JL-JLJLJF-J|F---7F------JLJ.L-7L7F7F7J-F||L-7LJLJF7F7L-7L-7L-7L7L--7F7L-JL-JL-JL-7F7|LJLJFJ7L.F-FF-JJ
L7-L7.777LLF---7|F-J|FJ|L7L--JLJLJL-----7F--7F7L--JL--7|L--7F-7F7FJJ7L7|||||7F7||F7L--7FJLJL-7L-7L-7|FL7F7LJL7F-7F-7F--7LJLJF---JF7L7L7.JJ.J
F|7.J..-7.LL7F7L7L--J|FJFJF---7F------7FJ|F7LJ|F7F7F-7|L---JL7|||7JJF7||||||FJLJLJ|F7-LJF7F7FL-7|F-J|F7LJL--7|L7|L7|L-7L---7L----JL-77.-J|7.
-J|7L77JLFFFJ|L7L-7F7LJJL-JF7|||F-----JL-J||F7||LJ|L7|L------JLJL-7.|LJLJLJ||F---7||L---JLJL---JLJF7LJL-----JL-J|FJL-7L-7F7L-7F7F7F-J--J.FJ.
|JLF.|J|F-LL-J7L-7LJL-7F7F-JL7LJL7F7-F--7FJLJ||L7LL7||F7F7F--7F7F7|-L7F7F-7|||F-7||L---------7F7F-J|F7F--------7|L-7FJF7LJL7.LJLJLJ.J.LF-JJ.
L7LL7JF-L-FF7F7F7L---7||||F-7|F7JLJL-JF-J|F--JL7L-7||||LJ|L-7||||LJF7LJ||.LJLJL7||L-7F-7F----J||L7FLJLJF------7||F7||FJ|F-7L--7F7.LF|---J7.F
LJF-JFF.|FFJ||LJL7F--J|||LJFJLJL-7F--7L--JL--7JL--J||||F7L--JLJLJ.FJL--JL-7F7F7|LJF7|L7LJF7F-7|L7L7F-7FJF--7F7LJLJLJLJJLJFJF7FJ|L---7..|.--J
L7J.FJ|LF7L7LJF-7LJF-7LJL7FJF7F-7|L-7|F-7F7F7L----7LJ|||L7F7F7F7F7L----7F-J|||||F7|LJL|F7|LJLLJ-L-JL7|L-JF-J|L7F7JF-7F--7L-JLJFJF-7FJ777...|
.L|FLJL.||LL--J|L7FJLL--7LJFJLJFJL--JLJ-|||||F7F7FJF7LJL7LJLJLJ|||F7F7FJL7L|LJ|LJ||7F7||LJF7-F7F7FF7||F7FL-7L7LJ|FJFJ|F-JF7F--JFJ7LJLF-7---J
|||LJ..F|L7F7F7F7LJF----JF7|F7FJF--7F7F7LJLJLJLJ||FJL--7|F-----J|||LJLJF7L7L-7L7FJL7||LJF-JL-JLJ|FJLJLJL---JFJF-JL7L-JL--J||F--JF7F7-7J77.F|
LJJ.|.-FJFJ||||||F7L----7|LJ||L-JF7LJLJL-7F--7F7LJL7F--J|L---7F7||L-7F-JL7|F7L7||F-J||F7L7F----7LJF-7F-7F7F7|FJLF-JF------J||-F7|LJL7J|FJ-FJ
FF|-|.|L7L-JLJLJLJ|F77F7LJF-JL---JL----7FJ|F-J||F7F|L7|FJF7F7LJ||L7LLJ-F7||||FJ||L7FJ||L7LJFF7|L--JJ||7LJLJLJL-7|F7L7F7F7F7||FJLJF--JJL|FFJJ
FFJF--F-JF-7F----7|||FJ|F7L----7F-----7|L-JL--JLJL7L7|FJFJ||L-7|L7|F7F7|LJLJ|L7||FJL7||FJFF-JL------J|F----7F-7LJ|L-J|LJLJLJLJF7FJF7..FF7J.|
FF7JJ7L7FJLLJF7F-JLJ|L7||L7F-77LJF--7FJL-------7F-JL|LJFJFLJF7LJ-||||||L--7FJ7||||-FJ|||F7L--7F7F7F7FJL---7LJFJF7L7JFJF7F--7F7|LJ||L7F7|J7.F
J|L.L|JLJJ-FFJLJF7F7L-JLJFJL7|F7FJF7LJ7F7F7F--7||F-7L7FJF7.FJ|LF-J|||||F7FJL7FJ||L7L7||LJL7F-J|LJ||||F----JF-JFJL7L-JFJ|L-7LJLJ-F7L7LJL7FJ-|
FFL7||7|L-F-JF-7|||L--7F-J|L||||L-JL---J||LJF-JLJL7L-JL7|L7L7L7L-7||||||||F-JL7||FJ-|LJF--JL--JF-J|LJL----7|F7L-7L---J.L-7L-----J|FJF-7L7-FF
F|7.J|LFJ-L--J.||||F--JL7F7FJLJL-7|F-7F7LJF7L-7LF7L--7FJL7L7|FJF-J||||LJLJL-7J||||F7|F-JF7F-7F7L--JF------JLJL-7L------7.L7F-7F-7LJFJ-L-J.FJ
L.L-|L7LLFF----J|LJL-7F7|||L----7L-JFJ|L-7|L-7L-J|F--J|F7|FJ|L7|F7LJ||F-7F--JFJLJ||||L-7||L7||L----JF7F7F-7F-7.L------7L-7|||LJJL-7L777|FF-J
.-..-FJJ.FJF--7FJF---J||LJL-7F-7L7F7L7|F7|L-7L7F7|L--7LJLJL-JFJ||L7FJLJFJ|F-7L--7LJLJF7||L7||L-----7|||LJFJL7L7F---7F7L--JLJF7-F77L-JL|LFJJ-
F--|JL7J.L7|F7||FL---7||F7F7|L7L-J|L7|||LJF-J|LJ||F--JF-----7L7LJ-||F-7L7||FJF-7L7F--J||L7|||-F-7F7||LJF-JF7L7||F--J|L7F-7-FJL-JL-7FL7|F-JJ.
LJLJ.LJLF7LJ|LJ|F----J|||LJ|L-JF--JFJLJL-7L--7F7LJL--7|LF7F7L-JF7FJ|L7L-J||L7L7L-JL--7LJFJ||L7L7||LJ|F-JF7||7||||F7F|FJL7L-JF7F---J7||77LL|7
FF-7.|.F|L7|L--JL7F-7FJLJF-JF--JF--JF7F7FJF--J|L7FF7FJL7|||L7F7|LJFJJL--7||FJFJF-7F--JF7L7LJFJFJ|L7FJL--JLJL-JLJLJL-JL--JF7FJ|L----77.F7--77
L|FL-J-FL7L-7F-7LLJ|LJF7FL--JF7-L---JLJ|L-JJF7|FJFJLJF-J|||FJ||L-7L-7FF7|LJL7|FJJ|L-7FJL7L-7L7L7||LJF---7F7F7F7F-7F------JLJ7L7F7F7L7..|.L|J
F|FJ.FF77L-7|L7|F7F---J|F77F-JL-7F7F---JF7F7|||L7L7F7L7FJLJL-JL-7L7FJFJ|L-7FJ|L-7|F7|L7FJF7|FJ7|L-7FJF-7LJLJLJLJFJL------7F-7L|||||FJ.7JJFJJ
J-77LL|L---JL7||||L---7LJL7L---7|||L--7FJ||LJ|L7L7LJ|FJ|F-------JFJL7L7L--JL7|F-JLJLJFJL7||||F-JF-JL-J|L-------7L--7F7F--JL7|7LJLJLJF-J|J-.|
JJL--LL-----7LJLJ||F7.L7F7L----JLJL---J|FJL-7L7L7L7FJL-JL7F----7FL-7L7L----7LJ|F--7F7L-7|||||L7FJF7F--7F---7F-7L--7LJ|L--7FJL7F-7JJ.L7LL7.LF
FFL|7-|.F---JF7F7L-JL--J|L7F----------7|L7F7|FJL|FJL-7F-7LJF---JF7.|FJLF7|FJF-JL7FJ||F7|||LJ|FJL7||L-7|L--7LJFJF-7L-7L---JL7FJ|FJ|J|7F.FF|.L
F7||LFFFL-7F7|||L-7F-7F7|FJ|F---------JL7LJ||L7FJ|F7F||-L--JLF7FJ|FJL7FJL7L7L-7FJ|FJ||LJ|L-7||F-J||F-JL---JF7L-JLL-7L------JL-JL7J.7-JL-7|L7
F|7F-LJF7L|||||||FJ|FJ||||FJL-7F7F-7-F77L-7||FJL7|||FJ|F7F--7||L7|L7FJ|F-JFJF-JL7|L7|L7FJF7|LJ|F7||L-7F7F--JL-----7L7F7F-7F7F---JLF|.F|LFJF7
.LL--J7|L-J|||LJFJFJL7|||LJF--J|LJJL7|L7F7|||L-7|||LJFJ|||F-J||FJ|FJL7|L7FJFJF-7|L7|L7|L7|LJF-J|||L7|LJLJF--------J-LJ||7LJ|L---7L7LF.|.J.L7
|JJJ.J7L-7FJLJFLL7|F-J|||F7L--7|F---J|FJ|||||F-J||L-7|7||||F7||L7||F-JL7||FJ-|FJ|FJ|FJL7|L7FJF7|||FJF7|F7L------7F---7|L--7|F-7FJFF7--7-L7J|
|JFF|.FLLLJLF-7F7|||F-JLJ|L---J|L7F-7|L7|||LJ|F7||F7|L7|||LJ|||FJ||L7F7||||F-J|FJL7||F7|L7||FJ|||||FJ|FJ|F-----7LJF--JL-7FJ|L7LJFFJ||FJ--.F|
|LJJ-LJ7|LJ|L7|||||||F---JF7F--JJ||.|L7||||F-J|LJ||||F|||L7FJ|||FJ|-||LJ||||-FJL-7|||||L7LJLJFJ||||L7||.|L-7F7F|F7L----7LJ-L7L---JFJJ7.|L|7|
F7J|.|JFL|JFF|LJLJ|||L7F--JLJF7F7||FJFJLJ||L-7L-7|||L7||L7||FJ||L7|FJL7FJ||L7L7F-JLJ||L7L---7L7|LJL7|||FJF7LJL7LJ|F7F-7L-7F-JF7F7FJJLF-7-J|L
FJFFFJL-7|JF7|F7F7|||7LJF----JLJLJ|L7L--7LJF-JF-JLJ|FJ|L7|||L7||7LJL7FJ|FJL7|FJL---7||FJF7F7|FJ|F--J|LJL7||F-7|F7LJ|L7L--JL--JLJ||J-FF7L.FJ7
|LF.L-7J-J-|LJ|LJ||||F--JF7F7F7F7FJJL7F7L-7|F7L---7|L7L7|LJ|FJLJF7F7||L|L-7|||F----J||L7|||||L7|L7F7L--7|||L7|LJL-7|FJF------7J.LJ7FJLJ|-FLJ
L||L7.7F77.L-7|F7||||L---JLJ||||||F--J|L7FJ||L7F-7|L7L7||F-J|.F-JLJLJL7L7FJ|||L--7F7||FJ|LJ|L7||FJ|L7F7|LJ|FJL-7F-JLJFJF-7F-7|JF.|JL-FLL.L-7
FLL.|-|LF----JLJ|||||F------J|LJ||L7F7L7|L7LJ.||L|L7|FJLJ|F7L7L--7F--7|FJL7LJL7F7LJ|||L7L-7L7|LJL7|FJ|||JFJL-7FJL7F--JFJFJL7|L77-L-JF-J|--L7
|7|F--LJL-7F7F7FJ||LJL----7F-JF-J|FJ|L7|L7L-7FJL7|FJLJ-LFJ|L7L-7FJL7F||L-7L-7||||F7|LJ7L7FJFJL7F7||L7||L7L7F-JL7FJ|F--J-|F-JL-J|FLJ7FJFJ.L||
|--F7FJ.|LLJLJLJJ||F------JL7FJF-JL7|FJ|FJF-JL7FJ||-F7-FJFJFJF7||F7|FJ|F-JF-JFJ|||LJF7F7|L7L7FJ|LJ|FJ||FJFJL7F-JL-JL-7F7LJ-L|-FL7J-7|L|.|F-.
7.F-J-JFF-J.|||--LJL------7FJ|FJF--J|L7|L7L--7LJ7|L7|L-JFJ.L7|||||LJL7|L-7L-7L-J|L-7|LJ|L7|FJL7L7FJL7|LJLL7FJ|F-7F7F7LJL7||FJ-L.7J|LFF7-LJ-|
FLJJ7|FJJ7.LLJF--|LF------J|LLJLL-7FJ|||FJF7FJ|F-JFJL-7FJ.FFJ|LJ|L7F7LJF7L7FJF--JF-J|F-J.||L7FJ.LJ|FJL7FF-J|LLJ|||||L7F7L77|J7|7L77-FJJ|.J.|
FJJL-7-J.77FJF7|FLFJF-7F7F7L-7F---J|F-J||FJLJF-JF7|-F-JL-7FJFJF-JFJ|L--JL-JL7L7F7L--JL--7LJFJ|.F--7L-7L7|F7L---7||||J||L7L7|J-|F7.LL-J.|7|FJ
F7FF-J|F--.L7-LF|-L7|.LJLJ|F7|L7F7FJ|F7||L--7L-7||L7L-7F-JL7|FJF7L7L--7F--7FJL|||F7F7F-7|-FJFJFJF7L--JFJLJL7F7FJLJLJFJL7L-J-7J|-77|7|.FL7JJ.
|--7LL|JFL-.77..LFLLJF7F--J|LJ.LJ|L7||||L-7FJF-J||FJF-JL--7|||FJL-JFF7LJF-JL-7||||LJ|L7|L7|FJ7L7|L7F7FJF---J||L-7F7FJF7L-7|7J..F77LL--|F-.FL
LL|L..7--J|F|7.L|LLF-JLJF-7L-77F7L-JLJ|L7L||7L7FJ|L7L7F7F-J|||L--7F-JL--JF7F7||||L-7|FJL7||L7F7||F|||L7L-7F7||F7LJ|L7||F7L77FJ-J.L-L-JL7--7J
7F--L7L7|.FJL|7-JFLL-7F7L7L7FJFJL-----JFJFJL-7|L7|FJLLJ||F-J||F-7||F7F7F7|LJLJ||L7FJLJF7||L7LJ|LJFJ|L7L7FJ||||||F7L7||||L7L7-|.LL-7-L.F|FJJ|
F|7FFJJ77F7-F7|FJJJ||||L-J||||L7F7F--7FJ|L7F7|L7|||-F--J|L7FJ|L7LJLJLJLJ|L---7||FJL-7FJ|||FJF7|F-JFJJL7||FJ|||||||FJ|||L7L-JFJ-L-7..|7FJL--J
-F-L|7LJL-J-LF|-J-F-L||F---JL7FJ|||F-J|.F7||LJFJ|||FJF-7|FJ|LL7L7F7F----JF7F7||||F-7LJFJLJ|FJLJL7FJ.F7LJ||FJ||||||L7LJL7L-77JJ|L||-LL-FJF.FJ
||F||7|.-..LFJL7.L-.LLJ|F-7F-JL7|LJL-7L7|LJL7FJFJLJL7|FJ|L7L7-L7||LJF-7F7|LJLJ|||L7L7FJFF-JL-7F-JL-7||F-J|L7|LJ|||FJL|L|F7L7.FF-JF.L|LJ7JFL.
--FJ77J||J.F7L-L-7F7JF7||JLJ7LFJL7F--JFJL-7FJL7|7FF-J||FJFJFJF-J||F7|JLJ|L---7|||FJ-LJF7L-7F-JL7F-7LJ|L7FJL||F7LJLJ|.|FJ|L-J7FJF7.F-F7J--||7
FFFJ.|--L.7.|.|.FLJ-F|LJL-7J|JL--JL7F7L--7||F-JL7FJF7||L7L7|JL-7|LJLJF--JF7F-JLJ|L----JL7FJL7LFJL7|F7|FJ|LFJLJL-----7-L-JJ|.F|LL77J.JJ7J-|J7
FF.F|J..|7F7FFFFJ|J-LL7F--JL-JLF---J||F-7|LJ|F7FJL-JLJ|FJ-||F--J|7F7FL7F7||L77-FJF---7F7|L--JFJF7|||LJ|FJFJF7F7F----J.||FLL-7J|LJF77|.|-FJ-L
7L-L7FF7-F7F---JFJF-JLLJ-JLFJJL|F-7FJ|L7|L-7|||L--7-F-JL7FJ|L7F7|FJL--J|||L7L-7L7L--7|||L7|LLL7|LJ|L-7||LL-J|||L-7J7|7J-F.JF|-FJ-F7-J-L-|J||
J77F|-LJ|LFLJ|J.-JFL7.|L7..J7F.LJFJL7|FJ|F-JLJ|F-7L7L--7|L-JFJ|||L7F7F7|LJFL7FJF|F--J||L-J--FFJL-7L--JLJJL|L|||F7|F|7.|L77-F7-J.FJ.F.FJJ|FL|
L7-F|.L-J7|LFJJFJ|7L7-F-J7F-J77.FJF7|||FJL--7FJL7L-JL|7|||F-JFJ||FJ|LJ|L--7FJ|FFJL7|7LJJJJ|F-L7F-JJL|J|J7||.LJLJLJ-JF-F7J7|L|JL--F7|-J7F77||
FL-J.FLJF-7JJ|FL7J-J|L|-FJ|J..LFL-JLJLJ|F7F7||F-JJ.L|FFJ|FJF7|FJ|L7L-7|F7FJL7L7L-7L--7-|-FFJJ-LJJJ-LLFF.77|-.L|.LF|-L7J|7L-7J7.JJL7||L-.J-J7
L..|FJJ.FJ|7L-J|L|F-7.F-J.--77F.L|7||LFJ|LJLJLJJ.|7-J|L-JL7||||FJL|F7|||LJF7L7L7FJF7FJ-L--J.|.L-J7F7J.J7|LLLJ-LJFJJLLJF-|-FJ||J|||.|-JFFJ.||
FJ.77JF---JJ||.7-F|-|7LJJ..FL7L7----J||FJLJ|-|-|.LF7-LLJ7FLJLJ|L7FJ||||||FJL-JFJ|FJLJJ77.LLLJ.LFF-JJ.F.|L.LJ|-LF-JJ.LJ7.L-7.|..LLJF7FL|-7|L-
LF7.F.|.LF7FL--L7LJ7.L7J.7.|.F-F.|LJLFLJ7LLJLJ7|.LJ7|||7FJFLF-JFJL7|||LJ-L-7F-J-||JJJF--7.LL.F.F|FJ.FL7|.-77|7.7.-77LL7-L7|F|-F7|FLL7|L|LF7|
.LJ|LJ|7|LF7JJ.L7.--7JL77|.F7J7L--.|.77.L-7J-LFF-FJL7--77-J7L7FJ7.LJ|L7J|FLLJJFL||J|F---LJ-L-7J-JJFF.L-77LF-|J-FLJ|FF.||FJ-|JJ||LFJ.-7L7.FJ7
|-|||JF-7-7||LJ7J-|7|..F7LFJ7.F7F|.F7.---7||J.|L.F-77L|-|7F7FLJ.L7FLL-JFF7J|-F7L||7LJJ||||||LJ|F7FLFJJJ||7J|.LFFJLL7JFL-7J7L-F||.JF|FJ-|7L|-
|.LFJ-|JLF7-7-||L|||J.FFJ7.|F-7J|7.LL-7|FJF-7F||FF7||7L-|-LJLJLF.F|-|JL--7F77F--||-.LFJ-LL7F-FF.FL--JJ.LJ7-F.F7F7L||.-.FJLF.-J|-FJJL7..J|FFJ
F-|.F7|.FJ7FL-|-7F||L-J|F7F-L7J-7--F7FFLJLFFL7J|7|F-7F|.|LF7|.L|-LLJFJJ..L-JF7|FLJ.F||J||-J.F-JFL.-7|F-JFF7.--JJJFJ|||-|F|L-.FJLLJL7LFF-L|J7
.FJF|JFFJLL77||L-7LJ77F-||L-|J.||J.L7-7-L--77F7L-J7JL--7L-F-|7-F7LF-L7LFF-J.||7FL|7.F--J7F|.F777-LL7LL.|LF7-LFJLF7|L7|.LJ777F|-7|-FJ-.L7-7||
F-J-L--|.LFJ-F|-J-----|.LLLJL7-JJ.F-L-7-F---JLJLLLL.7LL|LFJ|L--LL---L7-FJ.L|--L-JLL7L7.LLLJ-FJL|J-LLJL.|.JJLLLJ.LLF.L77LL|-J-|-7JJ..L-7JJ.-J
"""


if __name__ == "__main__":
    main()
