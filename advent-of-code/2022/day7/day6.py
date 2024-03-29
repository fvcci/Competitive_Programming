from pprint import pprint
from collections import defaultdict

total = 70000000
unused = 30000000


def solve (s):
    path, dirs = [], defaultdict(int)

    for l in s:
        if l[0] == "$":
            if l[1] == "cd":
                if l[2] == "..":
                    path.pop()
                else:
                    print(l[2])
                    path.append(l[2])
        elif l[0] != "dir":
            for i in range(len(path)):
                dirs[tuple(path[: i + 1])] += int(l[0])

    print(sum(size for size in dirs.values() if size <= 100000))

    required = 30000000 - (70000000 - dirs[("/",)])

    print(min(size for size in dirs.values() if size >= required))
    # pwd = []
    # dir_sizes = {}
    # for i in range(len(s)):
    #     try:
    #         l = s[i]
    #         # commands
    #         match l[1]:
    #             "cd":
    #                 if l[2]=="..":
    #                     pwd.pop()
    #                 elif l[2]=="/":
    #                     pwd = ["/"]
    #                 else:
    #                     pwd.append(l[2])
    #             # parse the directors given by ls
    #             "ls":
    #                 i += 1
    #                 while i<len(s) and s[i][0]!="$":
    #                     # add the sizes to the directory
    #                     if s[i][0]=="dir":
    #                         i += 1
    #                         continue

    #                     # trickle the number down the whole directory
    #                     for j in range(1, len(pwd)+1):
    #                         tup = " ".join(pwd[:j])
    #                         if tup not in dir_sizes:
    #                             dir_sizes[tup] = 0
    #                         dir_sizes[tup] += int(s[i][0])

    #                     i += 1
    #     except:
    #         print(i, l)
    #         return

    # goal = unused - (total - dir_sizes["/"])
    # mini = total
    # for k, v in dir_sizes.items():
    #     if mini>v>=goal:
    #         mini = v

    # print(mini)


"""
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
"""
def main ():
    with open("input.txt", "r") as f:
        solve([line.split() for line in f.readlines()])


if __name__=="__main__":
    main()

