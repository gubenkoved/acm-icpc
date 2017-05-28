# pylint: disable=invalid-name, C0111

import sys

def reachable_word(m, src, trg):
    if len(src) != len(trg):
        return False
    
    for i in range(len(src)):
        trg_letter = trg[i]
        src_letter = src[i]

        if src_letter == trg_letter:
            continue

        if src_letter not in m or trg_letter not in m[src_letter]:
            return False

    return True


def build_reachability_map(assoc):
    rm = {}

    for a in assoc:
        (src, trg) = (a[0], a[1])
        if src in rm:
            rm[src].add(trg)
        else:
            rm[src] = set(trg)

    return rm

def propogate_transitive(m):

    for k1 in m.keys():
        for k2 in m.keys():
            if k1 in m[k2]:
                m[k2] = m[k2] | m[k1]


def read_all_test():
    return """3 3
a c
b a
a b
aaa abc
abc aaa
acm bcm""".splitlines()

def read_all():
    #return read_all_test()
    return "".join(sys.stdin.readlines()).strip()

# print('hi there!')

# lines = read_all()

l1 = sys.stdin.readline().split(' ')

#print(lines[0])

(m, n) = (int(l1[0]), int(l1[1]))

assoc = [0] * m
words = [0] * n

for i in range(m):
    # l = lines[i + 1].split(' ')
    l = sys.stdin.readline().strip().split(' ')
    assoc[i] = [l[0], l[1]]

# print(assoc)

rm = build_reachability_map(assoc)

for i in range(m):
    propogate_transitive(rm)

# print(rm)

to_test = []

for i in range(n):
    #l = lines[m + 1 + i].split(' ')
    l = sys.stdin.readline().strip().split(' ')
    to_test.append([l[0], l[1]])

for i in range(n):
    # print('test {0} -> {1}'.format(to_test[0], to_test[1]))
    res = 'yes' if reachable_word(rm, to_test[i][0], to_test[i][1]) else 'no'
    print(res)