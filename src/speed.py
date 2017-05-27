import sys

def findZero2(f, a, b, z = 0):
	c = (a + b) / 2

	fa = f(a)
	fc = f(c)
	fb = f(b)

	if abs(fc) < 0.00000000001 or z > 950:
		return c

	if fc * fa < 0:
		return findZero2(f, a, c, z + 1)
	else:
		return findZero2(f, c, b, z + 1)

def solve(d, s, t):

	# compose f
	# compose mix x, max x
	# try to find zero

	minX = -min(s) + 0.001
	maxX = sum(d) / t - min(s)

	f = lambda x: f2(d, s, t, x)

	return findZero2(f, minX, maxX)

def f2(d, s, t, x):
	n = len(d)
	f = 0

	for i in range(n):
		f += d[i] / (s[i] + x)

	f -= t

	return f


# xr = findZero( lambda x: 10.45 - x, -1000, 1000 )
# xr = findZero2( lambda x: 10.45 - x ** 2, -1000, 1000 )

# x = solve([1, 10], [50, 10], 31 / 60)
# x = solve([4, 4, 10], [-1, 0, 3], 5)
# x = solve([5, 2, 3, 3], [3, 2, 6, 1], 10)

l = sys.stdin.readline().split(' ')

n = int(l[0])
t = int(l[1])

d = [0] * n
s = [0] * n

for i in range(n):
    l = sys.stdin.readline().split()
    
    d[i] = int(l[0])
    s[i] = int(l[1])

    i += 1

x = solve(d, s, t)

print(x)

exit(0)