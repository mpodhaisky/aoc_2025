import time
from collections import Counter, defaultdict
import hashlib
import re
from math import sqrt, gcd, lcm, inf
from heapq import heappop, heappush, heapify
import builtins
import sys
import requests
import os
import textwrap
from bs4 import BeautifulSoup
from functools import cache
from copy import deepcopy

AOC_SESSION = os.getenv("AOC_SESSION")
if not AOC_SESSION:
    raise RuntimeError("AOC_SESSION not set in environment")

def submit_answer(year: int, day: int, answer: str, part: int = 1):
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    cookies = {"session": AOC_SESSION}
    data = {
        "level": part,
        "answer": answer.strip(),
    }

    r = requests.post(url, cookies=cookies, data=data)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    article = soup.find("article")
    clean_text = article.get_text(separator=" ", strip=True)
    print(textwrap.fill(clean_text, width=80))

_last_printed = None
_real_print = builtins.print

def print(*args, **kwargs):
    global _last_printed
    text = " ".join(str(a) for a in args)
    _last_printed = text
    _real_print(text, **kwargs)

adj4 = [(-1,0),(0,1),(1,0),(0,-1)]
adj8 = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

def ask(prompt: str) -> str:
    with open("/dev/tty", "r+") as tty:
        tty.write(prompt)
        tty.flush()
        return tty.readline().strip()

def maybe_submit():
    res = _last_printed
    resp = ask(f"Do you want to submit \033[1m{_last_printed}\033[0m ? [1/2] ")
    year, day = map(int, sys.argv[1:])
    if resp.lower()=="1":
        submit_answer(year,day,res,1)
    elif resp.lower()=="2":
        submit_answer(year,day,res,2)

    
# trans={"U":(-1,0),"L":(0,-1), "D":(1,0),"R":(0,1)}
def nums(line):
    return list(map(int,re.findall(r'-?\d+', line)))

def solve(data: str):
    res=0
    A=[]
    X=set()
    Y=set()
    for line in data.split("\n"):
        A.append(nums(line))
        a,b = nums(line)
        X.add(a)
        Y.add(b)

    
    DX=list(range(len(X)))
    DY=list(range(len(Y)))

    transx = {}
    for i, x in enumerate(sorted(X)):
        transx[x]=i

    transy={}
    for i, y in enumerate(sorted(Y)):
        transy[y]=i
    
    grid = [list(".")*(max(DY)+1) for _ in range(max(DX)+1)]
    

    for i in range(len(A)):
        (a,b) ,(c,d)= sorted([A[i-1],A[i]])

        for x in range(transx[a],transx[c]+1):
            for y in range(transy[b],transy[d]+1):
                grid[x][y]="X"
    
    q= [(100,100)]
    grid[100][100]="X"
    for r, c in q:
        for dr, dc in adj4:
            if grid[r+dr][c+dc]!="X":
                grid[r+dr][c+dc]="X"
                q.append((r+dr,c+dc))
    
    M,N = len(grid),len(grid[0])    
    dp=[[0 for _ in range(N+1)] for _ in range(M+1)]

    for r in range(M):
        for c in range(N):
            dp[r+1][c+1] = (grid[r][c]=="X") + dp[r][c+1]
    
    for r in range(M):
        for c in range(N):
            dp[r+1][c+1]+=dp[r+1][c]
    
    dist=0
    for i, (a, b) in enumerate(A):
        for c, d in A:
            mx, Mx = min(transx[a],transx[c]),max(transx[a],transx[c])
            my, My = min(transy[b],transy[d]), max(transy[b],transy[d])
            area = dp[Mx+1][My+1] + dp[mx][my]-dp[Mx+1][my]-dp[mx][My+1]
            if area == (Mx-mx+1)*(My-my+1):
                if (abs(a-c)+1)*(abs(b-d)+1)> dist:
                    dist=(abs(a-c)+1)*(abs(b-d)+1)
    
    print(dist)
    
    

    
    
    


if __name__ == "__main__":
    data = open(0).read().rstrip()
    solve(data)
    maybe_submit()