import random
def function(x):
    return -x**3-x+3

# 使用遗传算法求解最大值
def genetic_algorithm():
    population = [random.random()*6-3 for _ in range(100)]

    for _ in range(iternum):
        population.sort(key=function, reverse=True)
        childs = []
        while (len(childs) < 100):
            father = population[random.randint(0,100//2)]
            mother = population[random.randint(0,100//2)]
            child = father * 0.8 + mother * 0.2
            if random.random() < 0.1:
                child = random.random()*6-3
            childs.append(child)
        population = childs
    return population

iternum = 200
pops = genetic_algorithm()
pops.sort(key=function, reverse=True)
print(pops[0], function(pops[0]))


