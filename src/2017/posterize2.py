import sys
from datetime import datetime

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def f(p: list, v: list) -> object:
    err = 0

    for p_cur in p:
        color = p_cur[0]
        amount = p_cur[1]
        closest_color = closest(color, v)
        err += amount * (color - closest_color) ** 2

    return err

def closest(color: int, v: list) -> int:
    for delta in range(256):
        if color + delta < 256 and v[color + delta] != 0:
            return color + delta
        elif color - delta >= 0 and v[color - delta] != 0:
            return color - delta

    eprint("here?!")
    raise "unable to find closest!"

def get_active(v: list):
    return to_print(v)

def enhanse(p: list, v: list):
    active_colors = get_active(v)

    n = len(active_colors)

    for color in active_colors:
        betterColor = None
        betterF = None

        for delta in range(-1, 2):

            if delta < 0:
                newColor = l(v, color)

            elif delta > 0:
                newColor = r(v, color)
            else:
                newColor = color

            if newColor is None:
                continue

            v[color] = 0
            v[newColor] = 1

            curF = f(p, v)

            # return back!
            v[newColor] = 0
            v[color] = 1

            if betterF is None or curF < betterF:
                betterColor = newColor
                betterF = curF

        v[color] = 0
        v[betterColor] = 1

    pass

def l(v: list, idx: int):
    for x in range(idx, -1, -1):
        if v[x] == 0:
            return x
    return None

def r(v: list, idx: int):
    for x in range(idx, 256):
        if v[x] == 0:
            return x
    return None

def init(p: list, k: int) -> list:
    n = 256
    v = [1 for x in range(n)]
    gains = [None] * n

    vActiveIndicies = set([x for x in range(n)])

    # leave only k
    for i in range(256 - k):
        # choose one that yields min gain
        fBefore = f(p, v)

        for idx in vActiveIndicies:

            v[idx] = 0
            gains[idx] = f(p, v) - fBefore
            v[idx] = 1

        minGain = positive_min(gains)
        minGainIdx = gains.index(minGain)

        # get rid of v = minGainIdx
        #v = v[:minGainIdx] + v[minGainIdx + 1:]
        eprint("exclude {0}".format(minGainIdx))
        v[minGainIdx] = 0
        gains[minGainIdx] = -1
        vActiveIndicies.remove(minGainIdx)

    return v

def positive_min(a: list):
    min = None
    for i in range(len(a)):
        if a[i] >= 0 and (min is None or a[i] < min):
            min = a[i]

    return min

def to_print(v: list):
    print_version = []
    for idx in range(256):
        if v[idx] == 1:
            print_version.append(idx)

    return print_version

# reading problem
firstLine = sys.stdin.readline()
firstLineSplit = firstLine.split(' ')

(d, k) = (int(firstLineSplit[0]), int(firstLineSplit[1]))

p = [None] * d

for i in range(d):
    ls = sys.stdin.readline().split(' ')
    p[i] = [int(ls[0]), int(ls[1])]

start = datetime.now()

# init K positions

# Naive approach -- did not work out
# pSorted = sorted(p, key= lambda x: x[1], reverse=True)

# v = [pSorted[x][0] for x in range(k)]
v = init(p, k)
# v = [x * int(255/k) for x in range(k)]

eprint("init v {0}".format(to_print(v)))

fPrev = None
cntr = 1

for round in range(100000):
    fCur = f(p, v)
    eprint('round #{0}, val: {1}'.format(round, fCur))
    enhanse(p, v)

    if fCur == fPrev:
        if cntr == 0:
            break
        else:
            cntr -= 1
    else:
        fPrev = fCur

# check if v has duplicates
eprint(to_print(v))
print(f(p, v))

end = datetime.now()
eprint("running for {0:.2f}".format((end - start).total_seconds()))