import re, math, copy, hashlib, operator, functools
from string import ascii_uppercase, ascii_lowercase
from collections import Counter, defaultdict, deque, namedtuple
from itertools import count, product, permutations, combinations, combinations_with_replacement

from utils import aoc_submit
from utils.utils import parse_line, parse_nums, mul, all_unique, factors, memoize, primes, resolve_mapping
from utils.utils import chunks, parts, gcd, lcm, print_grid, min_max_xy
from utils.utils import new_table, transposed, rotated, firsts, lasts
from utils.utils import md5, sha256, VOWELS, CONSONANTS
from utils.utils import Point, DIRS, DIRS_4, DIRS_8, N, NE, E, SE, S, SW, W, NW


input_str, aoc = aoc_submit({'day': 1, 'year': 2021})

lines = [line.strip() for line in input_str.strip().split('\n')]
print(lines)
lines = [int(l) for l in lines]

ans = 0
li = lines[0]
for l in lines:
  if l > li:
    ans += 1
  li = l

aoc(ans, l=1)

ans = 0
li = sum(lines[0:3])
for i in range(3, len(lines)):
  if li + lines[i] - lines[i-3] > li:
    ans += 1
  li += lines[i] - lines[i-3]

aoc(ans, l=2)
