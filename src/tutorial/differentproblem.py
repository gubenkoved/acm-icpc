import sys

for line in sys.stdin.readlines():
    # print('Line was:')
    # print(line)
    (a, b) = (int(line.split(' ')[0]), int(line.split(' ')[1]))
    print(abs(a - b))
