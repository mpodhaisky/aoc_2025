from math import prod
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

    A = []
    for line in data.split("\n"):
        A.append(nums(line))
    parent = list(range(len(A)))

    def find(x):
        if parent[x]!=x:
            parent[x]=find(parent[x])
        return parent[x]
    
    adj=[]
    for i in range(len(A)):
        for j in range(i+1,len(A)):
            a,b,c = A[i]
            d,e,f = A[j]
            heappush(adj,(pow(a-d,2)+pow(b-e,2)+pow(c-f,2),i,j))
    
    while True:
        l, a, b = heappop(adj)
        if find(a) ==find(b): continue
        parent[find(a)]=find(b)
        if len(set(map(find,parent))) == 1:
            print(A[a][0]*A[b][0])
            return


if __name__ == "__main__":
    data = open(0).read().rstrip()
    solve(data)
    maybe_submit()