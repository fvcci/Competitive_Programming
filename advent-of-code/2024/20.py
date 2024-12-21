import copy
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pprint import pprint

from tqdm import tqdm


@dataclass(frozen=True, eq=True)
class Coords:
    r: int
    c: int

    def add(self, coords):
        return Coords(self.r + coords.r, self.c + coords.c)

    def in_bounds(self, grid):
        return 0 <= self.r < len(grid) and 0 <= self.c < len(grid[0])


d = [Coords(-1, 0), Coords(0, -1), Coords(1, 0), Coords(0, 1)]


def main(inp):
    """
    bfs, and for each iteration have a possibility of
    cheating. When cheating starts, (when indicator shows
    that a process is cheating), it must decrement. Otherwise,
    it can decide whether to cheat or not to cheat.

    only enable cheat when you wanna clip into walls
    """
    mat = [list(a) for a in inp.split("\n")]
    start = None
    end = None
    for r in range(len(mat)):
        for c in range(len(mat[0])):
            if mat[r][c] == "S":
                start = Coords(r, c)
            if mat[r][c] == "E":
                end = Coords(r, c)

    """
    iterate through all the different ways to remove 2 adjacent walls
    run dfs each time and compare it to a base stime
    then saved time would be whether the new time is less than og time by 100 seconds
    """
    # find paths in the grid that have pattern .#. and replace it with
    # ... then check with bfs to find a path to the end

    def bfs(s, grid):
        q = deque()
        q.append(start)
        dis = [[float("inf") for _ in range(len(grid[0]))] for _ in range(len(grid))]
        dis[start.r][start.c] = 0
        parent = dict()
        parent[start] = None

        while q:
            cur = q.popleft()

            for dr in d:
                nxt = cur.add(dr)
                if not nxt.in_bounds(grid):
                    continue
                if grid[nxt.r][nxt.c] in [".", "E"] and dis[nxt.r][nxt.c] == float(
                    "inf"
                ):
                    dis[nxt.r][nxt.c] = dis[cur.r][cur.c] + 1
                    parent[nxt] = cur
                    q.append(nxt)
                    if grid[nxt.r][nxt.c] == "E":
                        # shortest_path = set()
                        # cur = end
                        # while cur is not None:
                        #     shortest_path.add(cur)
                        #     cur = parent[cur]

                        # pprint(dis)
                        # return dis[end.r][end.c], shortest_path
                        return dis[end.r][end.c]

        # pprint(dis)

        # shortest_path = set()
        # cur = end
        # while cur is not None:
        #     shortest_path.add(cur)
        #     cur = parent[cur]

        return dis[end.r][end.c]

    og_dis = bfs(start, mat)

    def print_grid(shortest_path):
        b = copy.deepcopy(mat)
        for c in shortest_path:
            b[c.r][c.c] = "^"
        pprint(["".join(g) for g in b])

    # ans = 0
    # vis = set()
    # cnt = defaultdict(int)
    # # find paths
    # for r in tqdm(range(len(mat))):
    #     for c in range(len(mat[0])):
    #         # iterate through 3 diff coords and take the unique ones and remove the middle hashtag
    #         for dr in d:
    #             it = Coords(r, c)
    #             sm = ""
    #             seq = list()
    #             for _ in range(3):
    #                 if not it.in_bounds(mat):
    #                     break
    #                 seq.append(it)
    #                 sm += mat[it.r][it.c]
    #                 it = it.add(dr)

    #             seq = tuple(seq)
    #             if (
    #                 sm in [".#.", ".#E", "S#."]
    #                 and seq not in vis
    #                 and seq[::-1] not in vis
    #             ):
    #                 vis.add(seq)
    #                 a = Coords(r, c).add(dr)
    #                 mat[a.r][a.c] = "."
    #                 new_dis = bfs(start)
    #                 cnt[og_dis - new_dis] += 1
    #                 ans += og_dis - new_dis >= 100
    #                 mat[a.r][a.c] = "#"

    ans = 0
    # ok so remove every square with side lengths 20 within range r and c
    # and iterate through every square that has this combination
    # record the path to get from one location to the other
    # if the shortest path contains the start and end points of the cheat, then we good
    # otherwise naahhh
    # ok nah this won't work too many issues with it
    # new_mat = copy.deepcopy(mat)
    # cnt = defaultdict(int)
    # vis = set()
    # for r in tqdm(range(len(mat))):
    #     for c in range(len(mat[0])):
    #         # iterate through squares within range r and c
    #         if mat[r][c] not in [".", "S"]:
    #             continue
    #         for sr in range(-20, 20):
    #             for sc in range(-20, 20):
    #                 if abs(sr) + abs(sc) > 20:
    #                     continue
    #                 ln = Coords(sr, sc)
    #                 bound = ln.add(Coords(r, c))
    #                 if not bound.in_bounds(mat):
    #                     continue
    #                 if mat[bound.r][bound.c] not in [".", "E"]:
    #                     continue
    #                 if (Coords(r, c), bound) in vis or (bound, Coords(r, c)) in vis:
    #                     continue

    #                 # replace everything in range from (r, c) to bound with "."
    #                 for i in range(min(r, bound.r), max(r, bound.r)):
    #                     for j in range(min(c, bound.c), max(c, bound.c)):
    #                         if mat[i][j] != "E":
    #                             new_mat[i][j] = "."

    #                 new_dis = bfs(start, new_mat)
    #                 ans += og_dis - new_dis >= 100
    #                 if og_dis - new_dis >= 50:
    #                     cnt[og_dis - new_dis] += 1

    #                 # then replace it back after finished
    #                 for i in range(min(r, bound.r), max(r, bound.r)):
    #                     for j in range(min(c, bound.c), max(c, bound.c)):
    #                         new_mat[i][j] = mat[i][j]

    # print(cnt)
    # print(ans)

    # what if we have a cost in our bfs that increments the count when all's said and done


test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

test2 = """"""

prod = """#############################################################################################################################################
#...#...#...###.....#.......#...###.....#.....###...###.........#...#...###...#...#.......###.....###.......###...#...#.......#.........#...#
#.#.#.#.#.#.###.###.#.#####.#.#.###.###.#.###.###.#.###.#######.#.#.#.#.###.#.#.#.#.#####.###.###.###.#####.###.#.#.#.#.#####.#.#######.#.#.#
#.#...#...#.....#...#.....#...#.#...#...#...#.#...#...#.#...#...#.#.#.#...#.#.#.#.#.....#...#...#.#...#.....#...#...#...#.....#.#.......#.#.#
#.###############.#######.#####.#.###.#####.#.#.#####.#.#.#.#.###.#.#.###.#.#.#.#.#####.###.###.#.#.###.#####.###########.#####.#.#######.#.#
#.............#...#...#...#...#.#...#.#...#.#...#.....#...#.#.....#.#...#.#.#...#.#...#.#...#...#...#...#...#...#.........#.....#.#...#...#.#
#############.#.###.#.#.###.#.#.###.#.#.#.#.#####.#########.#######.###.#.#.#####.#.#.#.#.###.#######.###.#.###.#.#########.#####.#.#.#.###.#
#.......#.....#.###.#.#...#.#...#...#...#...#.....#.....#...#...#...#...#.#...#...#.#.#.#...#...#...#...#.#...#.#.#...#...#.#.....#.#.#...#.#
#.#####.#.#####.###.#.###.#.#####.###########.#####.###.#.###.#.#.###.###.###.#.###.#.#.###.###.#.#.###.#.###.#.#.#.#.#.#.#.#.#####.#.###.#.#
#.....#.#.....#.#...#...#.#.....#.#.........#.#...#...#...#...#...###...#.###.#.....#.#.#...###...#...#.#...#.#.#...#...#.#.#...###.#.#...#.#
#####.#.#####.#.#.#####.#.#####.#.#.#######.#.#.#.###.#####.###########.#.###.#######.#.#.###########.#.###.#.#.#########.#.###.###.#.#.###.#
#...#.#.#.....#...#...#.#.#.....#.#.###.....#...#.#...#...#.#...#...#...#...#.#.......#.#.#...###...#.#.#...#.#.#.........#.#...#...#...#...#
#.#.#.#.#.#########.#.#.#.#.#####.#.###.#########.#.###.#.#.#.#.#.#.#.#####.#.#.#######.#.#.#.###.#.#.#.#.###.#.#.#########.#.###.#######.###
#.#.#.#.#.....#.....#.#.#.#.#...#...#...#...#.....#.#...#...#.#.#.#.#.....#...#...###...#.#.#.#...#.#.#.#...#.#.#.#.....#...#.....#.......###
#.#.#.#.#####.#.#####.#.#.#.#.#.#####.###.#.#.#####.#.#######.#.#.#.#####.#######.###.###.#.#.#.###.#.#.###.#.#.#.#.###.#.#########.#########
#.#.#.#.###...#.#.....#...#...#...###.....#.#.#...#.#.###...#.#...#.#...#.......#.....#...#.#.#.#...#.#...#.#.#.#.#.#...#...#.......#...#...#
#.#.#.#.###.###.#.###############.#########.#.#.#.#.#.###.#.#.#####.#.#.#######.#######.###.#.#.#.###.###.#.#.#.#.#.#.#####.#.#######.#.#.#.#
#.#...#.....#...#.........#...#...#...#.....#...#...#...#.#.#.....#.#.#.......#...#.....###.#.#.#...#...#.#.#.#.#...#.......#.........#...#.#
#.###########.###########.#.#.#.###.#.#.###############.#.#.#####.#.#.#######.###.#.#######.#.#.###.###.#.#.#.#.###########################.#
#.......#...#.#.....#...#.#.#...###.#.#.......#.....#...#.#...#...#.#.......#...#.#...#...#.#...#...#...#.#.#.#.#.....#.......#.....#.....#.#
#######.#.#.#.#.###.#.#.#.#.#######.#.#######.#.###.#.###.###.#.###.#######.###.#.###.#.#.#.#####.###.###.#.#.#.#.###.#.#####.#.###.#.###.#.#
#...###...#...#...#.#.#...#...#...#.#.###...#.#.###...#...#...#.#...###...#.#...#...#...#.#.....#...#.#...#.#.#.#...#...#...#...###.#...#...#
#.#.#############.#.#.#######.#.#.#.#.###.#.#.#.#######.###.###.#.#####.#.#.#.#####.#####.#####.###.#.#.###.#.#.###.#####.#.#######.###.#####
#.#.....#.........#.#.......#.#.#.#.#...#.#.#.#.......#.#...###.#...#...#...#.#####...#...#...#...#.#.#...#.#.#.#...###...#...#...#.....#...#
#.#####.#.#########.#######.#.#.#.#.###.#.#.#.#######.#.#.#####.###.#.#######.#######.#.###.#.###.#.#.###.#.#.#.#.#####.#####.#.#.#######.#.#
#.#.....#.....#...#.....#...#.#.#.#...#.#.#.#.#.......#.#.###...#...#.......#...#.....#...#.#...#.#.#...#.#.#.#.#.......#...#...#.#...#...#.#
#.#.#########.#.#.#####.#.###.#.#.###.#.#.#.#.#.#######.#.###.###.#########.###.#.#######.#.###.#.#.###.#.#.#.#.#########.#.#####.#.#.#.###.#
#.#.....#...#...#.....#.#...#.#.#.#...#.#.#.#.#.....#...#...#.#...#...#...#...#.#.#...#...#...#.#.#.....#...#...#.........#.....#.#.#.#.#...#
#.#####.#.#.#########.#.###.#.#.#.#.###.#.#.#.#####.#.#####.#.#.###.#.#.#.###.#.#.#.#.#.#####.#.#.###############.#############.#.#.#.#.#.###
#.#.....#.#.#.....#...#.....#...#.#.#...#.#.#.#.....#.....#.#.#.#...#.#.#.....#.#...#.#...#...#.#.......#.....#...###...#...###...#.#.#.#...#
#.#.#####.#.#.###.#.#############.#.#.###.#.#.#.#########.#.#.#.#.###.#.#######.#####.###.#.###.#######.#.###.#.#####.#.#.#.#######.#.#.###.#
#.#.###...#.#...#.#.............#...#...#.#.#.#.#.....#...#...#.#.#...#.#.......#...#.#...#...#.#.......#...#...###...#...#.........#...#...#
#.#.###.###.###.#.#############.#######.#.#.#.#.#.###.#.#######.#.#.###.#.#######.#.#.#.#####.#.#.#########.#######.#####################.###
#.#...#.#...#...#.......###.....#...#...#.#.#.#.#.#...#...#.....#.#.###.#.#...###.#.#.#.#...#.#.#.......#...###...#.#...............#...#...#
#.###.#.#.###.#########.###.#####.#.#.###.#.#.#.#.#.#####.#.#####.#.###.#.#.#.###.#.#.#.#.#.#.#.#######.#.#####.#.#.#.#############.#.#.###.#
#...#...#.....#...#...#...#.......#.#.#...#.#.#.#.#.....#.#...#...#...#.#.#.#.#...#.#.#.#.#.#.#.#...#...#.#...#.#...#.....#.....###.#.#.....#
###.###########.#.#.#.###.#########.#.#.###.#.#.#.#####.#.###.#.#####.#.#.#.#.#.###.#.#.#.#.#.#.#.#.#.###.#.#.#.#########.#.###.###.#.#######
###...#...#.....#...#...#...........#.#...#.#.#...#.....#.#...#.#...#.#.#...#.#...#.#.#.#.#...#.#.#.#.#...#.#.#.#.....#...#...#...#...#...###
#####.#.#.#.###########.#############.###.#.#.#####.#####.#.###.#.#.#.#.#####.###.#.#.#.#.#####.#.#.#.#.###.#.#.#.###.#.#####.###.#####.#.###
#...#...#.#.#...........#...#.......#...#.#.#.....#.#...#.#.#...#.#...#.....#.#...#.#.#.#...###...#.#.#.....#...#...#...#...#.#...#...#.#...#
#.#.#####.#.#.###########.#.#.#####.###.#.#.#####.#.#.#.#.#.#.###.#########.#.#.###.#.#.###.#######.#.#############.#####.#.#.#.###.#.#.###.#
#.#.......#.#.....#...#...#...#.....#...#.#.#...#.#.#.#.#.#.#...#.#...#.....#...#...#.#...#...#.....#.#.........#...#...#.#.#.#.#...#.#.#...#
#.#########.#####.#.#.#.#######.#####.###.#.#.#.#.#.#.#.#.#.###.#.#.#.#.#########.###.###.###.#.#####.#.#######.#.###.#.#.#.#.#.#.###.#.#.###
#.........#.....#...#.#.#.....#.....#.....#...#...#...#.#.#.#...#.#.#.#.........#...#.#...#...#.#...#.#.......#...#...#...#.#.#.#...#...#...#
#########.#####.#####.#.#.###.#####.###################.#.#.#.###.#.#.#########.###.#.#.###.###.#.#.#.#######.#####.#######.#.#.###.#######.#
#.....#...#.....#...#...#...#.#.....#...#...#...#...###...#.#...#...#.#...#.....###...#.#...#...#.#...###.....#...#.#.......#.#...#.#.......#
#.###.#.###.#####.#.#######.#.#.#####.#.#.#.#.#.#.#.#######.###.#####.#.#.#.###########.#.###.###.#######.#####.#.#.#.#######.###.#.#.#######
#...#.#.....###...#.###...#.#...#...#.#...#.#.#.#.#.#.....#...#...#...#.#.#.......#.....#...#.....#.....#.......#...#.....#...#...#.#.#.....#
###.#.#########.###.###.#.#.#####.#.#.#####.#.#.#.#.#.###.###.###.#.###.#.#######.#.#######.#######.###.#################.#.###.###.#.#.###.#
#...#.........#...#.#...#...#...#.#...#...#.#.#.#.#...#...###.....#.#...#.#.......#...#...#.###...#...#.#.................#...#.#...#...#...#
#.###########.###.#.#.#######.#.#.#####.#.#.#.#.#.#####.###########.#.###.#.#########.#.#.#.###.#.###.#.#.###################.#.#.#######.###
#.#.....#...#.....#...#.......#...#...#.#...#.#...#...#.......###...#...#.#.....#...#.#.#...#...#.....#...#...#.......###...#.#.#.#...#...###
#.#.###.#.#.###########.###########.#.#.#####.#####.#.#######.###.#####.#.#####.#.#.#.#.#####.#############.#.#.#####.###.#.#.#.#.#.#.#.#####
#.#.###...#.......#...#.#...........#.#.#...#.#.....#...#...#...#.....#.#.#...#...#.#...#...#.....#.........#...#...#.....#...#...#.#...#...#
#.#.#############.#.#.#.#.###########.#.#.#.#.#.#######.#.#.###.#####.#.#.#.#.#####.#####.#.#####.#.#############.#.###############.#####.#.#
#...#.......#.....#.#...#...........#...#.#.#.#.###...#...#.....###...#.#.#.#.#...#.#.....#.......#.#.............#.#.......#.....#...###.#.#
#####.#####.#.#####.###############.#####.#.#.#.###.#.#############.###.#.#.#.#.#.#.#.#############.#.#############.#.#####.#.###.###.###.#.#
#...#.....#.#.......###...#.........#...#.#...#...#.#.............#...#.#.#.#...#...#...#.....#...#.#.............#.#.....#.#...#...#...#.#.#
#.#.#####.#.###########.#.#.#########.#.#.#######.#.#############.###.#.#.#.###########.#.###.#.#.#.#############.#.#####.#.###.###.###.#.#.#
#.#.......#...#...#...#.#.#...........#...#######...#.............###...#...#...#...###...###...#...#...#.........#...#...#.#...#...#...#.#.#
#.###########.#.#.#.#.#.#.###########################.#######################.#.#.#.#################.#.#.###########.#.###.#.###.###.###.#.#
#...........#...#.#.#...#.........#E#############...#...............#.........#.#.#.#...#...#...#...#.#...###...#...#.#...#.#...#...#.....#.#
###########.#####.#.#############.#.#############.#.###############.#.#########.#.#.#.#.#.#.#.#.#.#.#.#######.#.#.#.#.###.#.###.###.#######.#
###...#...#.....#...#.....#.....#...#############.#.#...#...........#.#...#...#.#.#.#.#.#.#...#...#...#.......#...#.#.#...#...#...#...#.....#
###.#.#.#.#####.#####.###.#.###.#################.#.#.#.#.###########.#.#.#.#.#.#.#.#.#.#.#############.###########.#.#.#####.###.###.#.#####
#...#...#.......#...#...#.#...#.......###########.#...#.#...........#.#.#.#.#.#...#...#...#...#...#.....#...#.......#...###...#...#...#.....#
#.###############.#.###.#.###.#######.###########.#####.###########.#.#.#.#.#.#############.#.#.#.#.#####.#.#.#############.###.###.#######.#
#.............#...#...#.#...#.#...#...###########.....#.#.....#.....#...#...#.#...#.......#.#...#...###...#.#.............#.....###.....#...#
#############.#.#####.#.###.#.#.#.#.#################.#.#.###.#.#############.#.#.#.#####.#.###########.###.#############.#############.#.###
#...........#.#.#.....#.###...#.#...#...###########...#.#...#.#...#...#...###...#...#.....#.#.........#...#.#.............#...........#.#...#
#.#########.#.#.#.#####.#######.#####.#.###########.###.###.#.###.#.#.#.#.###########.#####.#.#######.###.#.#.#############.#########.#.###.#
#.........#.#.#.#.#...#.....#...#.....#.......#####...#.....#.#...#.#.#.#...#.....#...#...#.#...#...#.....#...###...#...###...#...#...#.....#
#########.#.#.#.#.#.#.#####.#.###.###########.#######.#######.#.###.#.#.###.#.###.#.###.#.#.###.#.#.#############.#.#.#.#####.#.#.#.#########
#...#...#.#...#.#.#.#.#.....#.....#...#.......#####S#.....#...#.#...#.#...#.#...#.#.#...#...###...#...............#...#...###.#.#...#.......#
#.#.#.#.#.#####.#.#.#.#.###########.#.#.###########.#####.#.###.#.###.###.#.###.#.#.#.###################################.###.#.#####.#####.#
#.#...#.#.......#.#.#.#...#.........#...#...###...#.#.....#.....#...#.###.#...#.#.#...#.............#...................#.....#...#...#...#.#
#.#####.#########.#.#.###.#.#############.#.###.#.#.#.#############.#.###.###.#.#.#####.###########.#.#################.#########.#.###.#.#.#
#.#...#...###...#...#.....#...............#.....#.#...#.....###...#.#...#...#...#.......#...#.....#.#...........#.....#.#.......#...#...#.#.#
#.#.#.###.###.#.#################################.#####.###.###.#.#.###.###.#############.#.#.###.#.###########.#.###.#.#.#####.#####.###.#.#
#.#.#...#.#...#...#...#.........................#.......#...#...#...#...###.....#...#...#.#.#.#...#.....#.....#...#...#.#.....#.#.....###.#.#
#.#.###.#.#.#####.#.#.#.#######################.#########.###.#######.#########.#.#.#.#.#.#.#.#.#######.#.###.#####.###.#####.#.#.#######.#.#
#.#.#...#.#.....#.#.#.#...............#.......#.#...#.....###.#...#...#.....###...#.#.#.#.#.#.#.......#...#...#.....###...#...#.#.......#...#
#.#.#.###.#####.#.#.#.###############.#.#####.#.#.#.#.#######.#.#.#.###.###.#######.#.#.#.#.#.#######.#####.###.#########.#.###.#######.#####
#...#...#.....#.#.#.#.#...#...........#.#.....#...#...#.....#...#.#...#.#...#.....#...#...#...#...#...#...#.....#...#...#...###.#.....#...###
#######.#####.#.#.#.#.#.#.#.###########.#.#############.###.#####.###.#.#.###.###.#############.#.#.###.#.#######.#.#.#.#######.#.###.###.###
#.....#.....#.#.#.#.#.#.#.#...........#.#.#...#...#.....#...#...#.#...#.#...#.#...#...#...#...#.#.#.....#.........#...#.......#.#...#...#...#
#.###.#####.#.#.#.#.#.#.#.###########.#.#.#.#.#.#.#.#####.###.#.#.#.###.###.#.#.###.#.#.#.#.#.#.#.###########################.#.###.###.###.#
#...#.......#...#...#...#.............#.#.#.#...#.#...#...###.#...#.....#...#.#.#...#...#.#.#.#.#.#...#.....#...........#.....#...#...#.#...#
###.###################################.#.#.#####.###.#.#####.###########.###.#.#.#######.#.#.#.#.#.#.#.###.#.#########.#.#######.###.#.#.###
###.........#.........#.................#...#...#.#...#.....#.......#...#...#.#.#.#.....#...#.#.#.#.#.#...#.#.........#.#.......#...#.#.#...#
###########.#.#######.#.#####################.#.#.#.#######.#######.#.#.###.#.#.#.#.###.#####.#.#.#.#.###.#.#########.#.#######.###.#.#.###.#
#.....#...#...#.....#...#...###...#...#...#...#...#.....#...#.....#...#.#...#.#.#...###.....#.#.#...#.....#...........#.......#...#...#.....#
#.###.#.#.#####.###.#####.#.###.#.#.#.#.#.#.###########.#.###.###.#####.#.###.#.###########.#.#.#############################.###.###########
#...#.#.#.#...#...#.###...#.....#.#.#...#...###...###...#...#...#.#...#.#...#.#.#.....#.....#.#...........................###.....#.......###
###.#.#.#.#.#.###.#.###.#########.#.###########.#.###.#####.###.#.#.#.#.###.#.#.#.###.#.#####.###########################.#########.#####.###
#...#...#...#.....#.#...#.......#.#...#...#.....#...#...#...#...#...#.#.#...#.#.#.#...#.....#...............#...........#...........#...#...#
#.#################.#.###.#####.#.###.#.#.#.#######.###.#.###.#######.#.#.###.#.#.#.#######.###############.#.#########.#############.#.###.#
#.................#.#.....#.....#.....#.#...#.......#...#...#.......#...#...#.#...#.#...###.......#.......#...#.......#...............#.....#
#################.#.#######.###########.#####.#######.#####.#######.#######.#.#####.#.#.#########.#.#####.#####.#####.#######################
###...#...###...#.#.....###...........#.#.....###...#...#...#.....#...#.....#...#...#.#.#...#...#...#...#.......#...#.......#...#...#...#...#
###.#.#.#.###.#.#.#####.#############.#.#.#######.#.###.#.###.###.###.#.#######.#.###.#.#.#.#.#.#####.#.#########.#.#######.#.#.#.#.#.#.#.#.#
#...#...#.....#...#...#...............#.#...#...#.#.#...#.#...#...###.#...#...#.#...#.#.#.#...#.#.....#.#.......#.#.......#...#...#...#...#.#
#.#################.#.#################.###.#.#.#.#.#.###.#.###.#####.###.#.#.#.###.#.#.#.#####.#.#####.#.#####.#.#######.#################.#
#.#.....#...#...#...#...#...#...#...###...#.#.#.#.#.#.#...#...#.#...#.#...#.#.#.#...#.#.#.#.....#.....#.#.....#.#.......#.#...............#.#
#.#.###.#.#.#.#.#.#####.#.#.#.#.#.#.#####.#.#.#.#.#.#.#.#####.#.#.#.#.#.###.#.#.#.###.#.#.#.#########.#.#####.#.#######.#.#.#############.#.#
#...###...#...#.#.#...#.#.#...#.#.#...#...#.#.#.#.#.#.#.#.....#.#.#.#.#...#.#.#.#...#.#...#...#...#...#.#...#.#.#...#...#.#...#.......#...#.#
###############.#.#.#.#.#.#####.#.###.#.###.#.#.#.#.#.#.#.#####.#.#.#.###.#.#.#.###.#.#######.#.#.#.###.#.#.#.#.#.#.#.###.###.#.#####.#.###.#
###...#...#.....#.#.#.#.#...#...#.#...#.#...#.#.#.#...#.#...###.#.#.#...#.#.#...#...#...#.....#.#.#.###...#...#...#.#.###...#...#.....#.....#
###.#.#.#.#.#####.#.#.#.###.#.###.#.###.#.###.#.#.#####.###.###.#.#.###.#.#.#####.#####.#.#####.#.#.###############.#.#####.#####.###########
#...#...#...#.....#.#...#...#...#.#...#.#.#...#.#.....#...#...#.#.#...#.#.#.....#.#.....#.#...#.#.#...............#.#...#...#...#...........#
#.###########.#####.#####.#####.#.###.#.#.#.###.#####.###.###.#.#.###.#.#.#####.#.#.#####.#.#.#.#.###############.#.###.#.###.#.###########.#
#.#...#.......###...#...#...#...#...#.#.#.#...#.#...#.#...#...#.#.#...#.#.#.....#.#...#...#.#.#.#.#...#.......#...#.....#...#.#.#.......#...#
#.#.#.#.#########.###.#.###.#.#####.#.#.#.###.#.#.#.#.#.###.###.#.#.###.#.#.#####.###.#.###.#.#.#.#.#.#.#####.#.###########.#.#.#.#####.#.###
#.#.#.#.#.........#...#...#.#...#...#...#.....#...#.#.#.#...#...#.#.....#...#.....#...#.#...#...#.#.#.#.....#.#.......#...#.#.#...#...#...###
#.#.#.#.#.#########.#####.#.###.#.#################.#.#.#.###.###.###########.#####.###.#.#######.#.#.#####.#.#######.#.#.#.#.#####.#.#######
#.#.#...#.......#...#.....#.#...#.#...#.............#.#.#...#...#.........#...#...#.###.#.#.....#.#.#.......#.......#.#.#...#.......#.......#
#.#.###########.#.###.#####.#.###.#.#.#.#############.#.###.###.#########.#.###.#.#.###.#.#.###.#.#.###############.#.#.###################.#
#...#...........#...#.#...#.#...#.#.#...#...#...#...#.#.....#...#.....#...#.#...#.#...#.#.#...#...#.#...#.........#...#...#.....#...#...#...#
#####.#############.#.#.#.#.###.#.#.#####.#.#.#.#.#.#.#######.###.###.#.###.#.###.###.#.#.###.#####.#.#.#.#######.#######.#.###.#.#.#.#.#.###
#.....#.....#...#...#.#.#...###.#.#.#.....#.#.#...#.#.......#...#...#.#...#.#.#...#...#...#...#...#...#...#.......#.....#.#.#...#.#...#.#...#
#.#####.###.#.#.#.###.#.#######.#.#.#.#####.#.#####.#######.###.###.#.###.#.#.#.###.#######.###.#.#########.#######.###.#.#.#.###.#####.###.#
#.#...#.###...#.#...#.#.#.......#.#...#.....#.#.....#.....#...#...#.#.#...#...#...#.......#...#.#.#...#...#.........#...#.#.#...#.....#...#.#
#.#.#.#.#######.###.#.#.#.#######.#####.#####.#.#####.###.###.###.#.#.#.#########.#######.###.#.#.#.#.#.#.###########.###.#.###.#####.###.#.#
#...#...#...#...#...#...#...#...#.###...#...#.#.....#...#.#...#...#.#.#.#...#.....#...#...#...#.#.#.#.#.#...#.......#...#...###...#...###...#
#########.#.#.###.#########.#.#.#.###.###.#.#.#####.###.#.#.###.###.#.#.#.#.#.#####.#.#.###.###.#.#.#.#.###.#.#####.###.#########.#.#########
#.........#...#...#.......#...#.#.#...#...#...###...#...#.#...#...#.#.#.#.#.#.#...#.#.#...#...#.#.#.#.#...#.#.....#...#.....#.....#.........#
#.#############.###.#####.#####.#.#.###.#########.###.###.###.###.#.#.#.#.#.#.#.#.#.#.###.###.#.#.#.#.###.#.#####.###.#####.#.#############.#
#...........#...###.....#.......#.#...#...#.......#...###.#...###...#.#...#.#...#...#.#...#...#.#.#.#.#...#.#...#...#.#.....#.#...#.....#...#
###########.#.#########.#########.###.###.#.#######.#####.#.#########.#####.#########.#.###.###.#.#.#.#.###.#.#.###.#.#.#####.#.#.#.###.#.###
#...#.......#.......###.......#...###.#...#.....#...#...#...###.......#...#.......###...###...#.#...#.#...#...#.#...#.#.....#...#.#.###.#...#
#.#.#.#############.#########.#.#####.#.#######.#.###.#.#######.#######.#.#######.###########.#.#####.###.#####.#.###.#####.#####.#.###.###.#
#.#.#.....#...#.....#.........#.###...#...#.....#.....#.......#.#...#...#...#...#...#...###...#...###...#.....#.#.###.....#.....#.#.#...#...#
#.#.#####.#.#.#.#####.#########.###.#####.#.#################.#.#.#.#.#####.#.#.###.#.#.###.#####.#####.#####.#.#.#######.#####.#.#.#.###.###
#.#.......#.#.#.....#.#...#...#.#...#...#.#...#...#...........#.#.#.#...#...#.#.....#.#.#...#...#.....#.......#.#...#...#.......#.#.#...#...#
#.#########.#.#####.#.#.#.#.#.#.#.###.#.#.###.#.#.#.###########.#.#.###.#.###.#######.#.#.###.#.#####.#########.###.#.#.#########.#.###.###.#
#.#...#...#.#.#...#.#.#.#...#.#.#.#...#.#.###...#.#...........#.#.#.#...#...#.#.......#...#...#.#...#.......###.....#.#.........#.#.#...#...#
#.#.#.#.#.#.#.#.#.#.#.#.#####.#.#.#.###.#.#######.###########.#.#.#.#.#####.#.#.###########.###.#.#.#######.#########.#########.#.#.#.###.###
#.#.#.#.#.#.#.#.#.#.#.#.#.....#.#.#...#.#.#.......#.....#...#.#.#.#.#.....#.#.#.#...#.....#...#.#.#...#...#...........#...#...#.#.#.#...#...#
#.#.#.#.#.#.#.#.#.#.#.#.#.#####.#.###.#.#.#.#######.###.#.#.#.#.#.#.#####.#.#.#.#.#.#.###.###.#.#.###.#.#.#############.#.#.#.#.#.#.###.###.#
#...#...#...#...#...#...#.......#.....#...#.........###...#...#...#.......#...#...#...###.....#...###...#...............#...#...#...###.....#
#############################################################################################################################################"""

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "prod":
        main(prod)
    elif a == "test":
        main(test)
    elif a == "test2":
        main(test2)
    else:
        assert False