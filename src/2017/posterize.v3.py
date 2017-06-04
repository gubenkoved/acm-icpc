import sys

# https://journal.r-project.org/archive/2011-2/RJournal_2011-2_Wang+Song.pdf

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def mean(lst: list):
    return sum(lst) / len(lst)

def sum_of_squared_differences_to(p: list, target: float):
    result = 0
    for i in range(len(p)):
        number = p[i][0]
        amount = p[i][1]
        result += amount * (number - target) ** 2
    return result

def weighted_mean(p: list):
    total_points_count = sum([x[1] for x in p])
    weighted_sum = sum([x[0]*x[1] for x in p])
    return round(weighted_sum / total_points_count, 0)

def sum_of_squared_differences_to_mean(p: list):
    return sum_of_squared_differences_to(p, weighted_mean(p))

def read_line():
    l = sys.stdin.readline()
    return [int(x) for x in l.split(' ')]

def precalculate_sums_of_squared_diffs_to_means(p: list):
    n = len(p)
    precalculated = [[None] * n for i in range(n)]

    for i in range(n):
        for j in range(i, n):
            points_range = p[i:j+1]
            precalculated[i][j] = sum_of_squared_differences_to_mean(points_range)

    return precalculated

def min_sum_of_squared_errors(p: list, k: int):
    n = len(p)
    # allocate array of (n + 1) rows and k + 1 columns
    # D[n][k] to be a solution of original problem
    D = [[None] * (k + 1) for i in range(n + 1)]

    d_precalculated = precalculate_sums_of_squared_diffs_to_means(p)

    # iterate trough row in columns (columns iterated in outer loop)
    for m in range(k + 1):
        for i in range(n + 1):
            if i == 0 or m == 0\
                    or m >= i: # num of clusters more than amount of points
                D[i][m] = 0
                continue

            # then number of cluster is 1 then solution is trivial -- mean
            if m == 1:
                #D[i][m] = sum_of_squared_differences_to_mean(p[0:i])
                D[i][m] = d_precalculated[0][i - 1]
                continue

            D_optimal = None

            for j in range(m, i + 1):
                #D_current = D[j - 1][m - 1] + df(p, j, i)
                D_current = D[j - 1][m - 1] + d_precalculated[j - 1][i - 1]

                if D_optimal is None or D_current < D_optimal:
                    D_optimal = D_current

            D[i][m] = D_optimal
    return D[n][k]

# print(weighted_mean([[50, 20], [150, 10]]))
#exit(0)


l = read_line()
(d, k) = (l[0], l[1])

# p contains list of lists ([color, num])
p = []

for i in range(d):
    l = read_line()
    p.append([l[0], l[1]])

eprint("d={0}, k={1}".format(d, k))
eprint("p={0}".format(p))

result = min_sum_of_squared_errors(p, k)
print("{0:.0f}".format(result))