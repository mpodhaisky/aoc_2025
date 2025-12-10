from collections import Counter, defaultdict, deque
import hashlib
import re
from math import sqrt, gcd, lcm, inf, prod
from heapq import heappop, heappush, heapify
import builtins
import sys
import requests
import os
import textwrap
from bs4 import BeautifulSoup
from functools import cache
from copy import deepcopy
from itertools import product, combinations_with_replacement
import numpy as np
from ortools.linear_solver import pywraplp
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
    res = 0.0

    for line in data.split("\n"):
        _, rest = line.split("] ")
        groups_str, rhs_str = rest.split(" {", 1)

        B = groups_str.split()
        B = list(map(nums, B))

        C = nums(rhs_str)

        m = len(C)
        for r, row in enumerate(B):
            cur = [0] * m
            for idx in row:
                cur[idx] = 1
            B[r] = cur

        n_vars = len(B)

        A_eq = np.array(list(zip(*B)), dtype=int)
        b_eq = np.array(C, dtype=int)

        solver = pywraplp.Solver.CreateSolver("CBC")

        x = [solver.IntVar(0, solver.infinity(), f"x_{j}") for j in range(n_vars)]

        for i_eq in range(m):
            lb = float(b_eq[i_eq])
            ub = float(b_eq[i_eq])
            ct = solver.Constraint(lb, ub, f"eq_{i_eq}")
            for j in range(n_vars):
                coeff = int(A_eq[i_eq, j])
                if coeff != 0:
                    ct.SetCoefficient(x[j], coeff)

        objective = solver.Objective()
        
        for var in x: objective.SetCoefficient(var, 1)
        objective.SetMinimization()
        solver.Solve()
        
        res += objective.Value()
        

    print(int(res))


if __name__ == "__main__":
    data = open(0).read().rstrip()
    solve(data)
    maybe_submit()