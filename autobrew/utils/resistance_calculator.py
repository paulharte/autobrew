
def res(r1, r2):
    return r1*r2/(r1+r2)

goal = 4700

choices = [1000000,100000,10000, 5100, 2000, 1000, 330]

best = 1000000

for r1 in choices:
    for r2 in choices:
        resistance = res(r1,r2)
        if abs(goal - resistance) < best:
            best = abs(goal - resistance)
            print('New best ' + str(resistance))
            print(r1)
            print(r2)
        