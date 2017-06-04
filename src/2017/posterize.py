import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def f(p: list, v: list) -> object:
    err = 0

    for p_cur in p:
        color = p_cur[0]
        amount = p_cur[1]
        #closest_color = sorted(v, key = lambda x: (color - x) ** 2 )[0]
        closest_color = closest(color, v)
        err += amount * (color - closest_color) ** 2

    return err

def closest(color: int, v: list) -> int:
    for delta in range(256):
        if color + delta < 256 and color + delta in v:
            return color + delta
        elif color - delta >= 0 and color - delta in v:
            return  color - delta

    eprint("here?!")
    raise "unable to find closest!"

def enhanse(p: list, v: list):
    n = len(v)

    for i in range(n):
        vInit = v[i]

        vBest = None
        fBest = None

        for delta in range(-1, 2):

            # vCurrent = vInit + delta

            if delta < 0:
                vCurrent = l(v, vInit)
            elif delta > 0:
                vCurrent = r(v, vInit)
            else:
                vCurrent = vInit

            if vCurrent is None:
                continue

            v[i] = vCurrent
            fCurrent = f(p, v)

            if fBest is None or fCurrent < fBest:
                vBest = vCurrent
                fBest = fCurrent

            v[i] = vBest

    pass

def enhanse2(p: list, v: list):
    n = len(v)

    fInit = f(p, v)

    bestProfit = 0
    bestIndex = None
    bestDelta = None

    for i in range(n):
        vInit = v[i]

        for delta in range(-1, 2):
            v[i] = vInit + delta
            fCurrent = f(p, v)
            profit = fInit - fCurrent

            if bestProfit is None or profit > bestProfit:
                bestProfit = profit
                bestIndex = i
                bestDelta = delta

            v[i] = vInit

    # modify only single one

    if bestProfit != 0:
        v[bestIndex] += bestDelta

    pass

def l(v: list, idx: int):
    for x in range(idx, -1, -1):
        if x not in v:
            return x
    return None

def r(v: list, idx: int):
    for x in range(idx, 256):
        if x not in v:
            return x
    return None

def init(p: list, k: int) -> list:

    v = [x for x in range(256)]

    # leave only k
    for i in range(256 - k):
        # choose one that yields min gain
        fBefore = f(p, v)
        gains = [None] * len(v)

        for j in range(len(v)):

            vNew = v[:]
            del vNew[j]

            gains[j] = f(p, vNew) - fBefore

        minGain = min(gains)
        minGainIdx = gains.index(minGain)

        # get rid of v = minGainIdx
        #v = v[:minGainIdx] + v[minGainIdx + 1:]
        eprint("exclude {0}".format(v[minGainIdx]))
        del v[minGainIdx]

    return v

# reading problem
firstLine = sys.stdin.readline()
firstLineSplit = firstLine.split(' ')

(d, k) = (int(firstLineSplit[0]), int(firstLineSplit[1]))

p = [None] * d

for i in range(d):
    ls = sys.stdin.readline().split(' ')
    p[i] = [int(ls[0]), int(ls[1])]

# init K positions

# Naive approach -- did not work out
pSorted = sorted(p, key= lambda x: x[1], reverse=True)

v = [pSorted[x][0] for x in range(k)]
# v = init(p, k)
# v = [x * int(255/k) for x in range(k)]

eprint("init v {0}".format(v))

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
if len(set(v)) != len(v):
    raise 'should not happen'
    exit(1)

eprint(v)
print(f(p, v))
