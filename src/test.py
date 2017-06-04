from datetime import datetime

def f():
    r = 0

    for i in range(100000):
        for j in range(10000):
            r += i * j

    return  r

print('starting!')

start = datetime.now()
print(f())
end= datetime.now()

print((end-start).total_seconds())