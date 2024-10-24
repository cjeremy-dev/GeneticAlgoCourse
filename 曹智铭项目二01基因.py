import random

genNum = 23
popNum = 100
def decode(s):
    x = int("0b"+s, 2)
    res = 6*x / (pow(2, genNum)-1)-3
    return res

def fitness(s):
    x = decode(s)
    return -x**2-x+3

def mutation(pop):
    res = []
    for s in pop:
        if (random.random() < 0.01):
            p = random.randint(0, genNum - 1)
            a = '0' if s[p] == '1' else '1'
            s = s[:p] + a + s[p+1:]
        res.append(s)
    return res


def select(pop):
    pop.sort(key=fitness, reverse=True)
    selected = pop[:popNum // 2] + pop[popNum // 2:popNum]
    return selected

def cross(pop):
    childs = []
    while len(childs) < popNum:
        a = random.randint(0, popNum - 1)
        b = random.randint(0, popNum - 1)
        child = pop[a][:genNum // 2] + pop[b][genNum // 2:]
        childs.append(child)
    return childs

def create():
    res = []
    st = "01"
    for _ in range(popNum):
        s = ""
        for j in range(genNum):
            s += st[random.randint(0, 1)]
        res.append(s)
    return res

def geneAlgo(max_iter):
    population = create()
    for _ in range(max_iter):
        population = select(population)
        nextgen = cross(population)
        nextgen = mutation(nextgen)
        population = nextgen
    return population

res = geneAlgo(200)
res.sort(key=fitness, reverse=True)
print(decode(res[0]), fitness(res[0]))