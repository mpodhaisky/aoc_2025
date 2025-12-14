from collections import Counter, defaultdict
import hashlib
import re
import math
from heapq import heappop, heappush, heapify

adj4 = [(-1,0),(0,1),(1,0),(0,-1)]
adj8 = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

# trans={"U":(-1,0),"L":(0,-1), "D":(1,0),"R":(0,1)}
def nums(line):
    return list(map(int,re.findall(r'-?\d+', line)))

def solve(data):
    res=0
    for line in data.split(","):
        a, b = map(int,line.split("-"))
        for n in range(a,b+1):
            n=str(n)
            l=len(n)
            if n[:l//2] == n[l//2:]:
                res+=int(n)
    print(res)
         


if __name__ == "__main__":
    data = open(0).read().rstrip()
    solve(data)