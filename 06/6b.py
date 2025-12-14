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
    grid=data.split("\n")
    M,N = len(grid),len(grid[0])
    grid[-1]+="  "
    
    grid = list(map(list,zip(*grid)))
    
    while grid:
        cur=[]
        op=None
        while grid[-1][-1] not in "+*":
            if set(grid[-1])!={" "}:
                
                cur.append("".join(grid.pop()))
            else:
                grid.pop()
        
        
        op=grid[-1][-1]
        grid[-1][-1]=" "
        cur.append("".join(grid.pop()))
        print(cur)
        res += eval(op.join(cur))
    print(res)
        

    return
    
    for r in range(M):
        for c in range(N):
            if grid[r][c] not in "*+":
                continue
            for dc in range(1,1000):
                if c+dc >= N or grid[r][c+dc] in "*+":
                    break
            dN = c+dc
            cur=[]
            for nc in range(c,dN):
                cur.append("")
                for nr in range(r):
                    if grid[nr][nc].isnumeric():
                        cur[-1]+=grid[nr][nc]
            
            print(cur)
            

    print(res)

    # for a, b, c,d, op in zip(B[0],B[1],B[2],B[3],ops.replace(" ","")):
    #     cur=[]
    #     #print(a,b,c)
    #     while a or b or c or d:
    #         cur.append("")
    #         a=str(a)
    #         b=str(b)
    #         c=str(c)
    #         d=str(d)
    #         if a: 
    #             cur[-1]+=a[-1]
    #             a=a[:-1]
    #         if b: 
    #             cur[-1]+=b[-1]
    #             b=b[:-1]
    #         if c: 
    #             cur[-1]+=c[-1]
    #             c=c[:-1]
    #         if d: 
    #             cur[-1]+=d[-1]
    #             d=d[:-1]
    #     print(cur)
    #     res+=eval(op.join(cur))

    
    # print(res)


if __name__ == "__main__":
    data = open(0).read().rstrip()
    solve(data)
    maybe_submit()