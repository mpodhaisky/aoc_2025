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
    cur=50
    res=0
    for line in data.split("\n"):
        op = line[0]
        n = nums(line)[0]
        for _ in range(n):
            if op =="L":    
                cur = (cur-1)%100
            else:
                cur = (cur + 1)%100
            if cur == 0:
                res+=1
        
        
    print(res)


if __name__ == "__main__":
    data = open(0).read().rstrip()
    solve(data)