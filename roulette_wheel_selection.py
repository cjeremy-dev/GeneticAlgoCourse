import numpy as np
import random
# import matplotlib.pyplot as plt

# 定义函数
def f(x):
    return x * np.sin(10 * np.pi * x) + 2

# 二进制字符串转浮点数
def binary_to_float(binary_str, min_val=-1, max_val=2):
    decimal = int(binary_str, 2)
    return min_val + (max_val - min_val) * decimal / (2**len(binary_str) - 1)

# 浮点数转二进制字符串
def float_to_binary(x, min_val=-1, max_val=2, precision=10):
    normalized_x = (x - min_val) / (max_val - min_val)
    binary_str = format(int(normalized_x * (2**precision - 1)), '0' + str(precision) + 'b')
    return binary_str

# 计算适应度
def fitness(individual):
    x = binary_to_float(individual, min_val=-1, max_val=2)
    return f(x)

# 轮盘赌选择
def roulette_wheel_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    probabilities = [f / total_fitness for f in fitnesses]
    cumulative_probabilities = np.cumsum(probabilities)
    r = random.random()
    for i, cp in enumerate(cumulative_probabilities):
        if r < cp:
            return population[i]

# 单点交叉
def single_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# 多点交叉
def multi_point_crossover(parent1, parent2, population):
    points = sorted(random.sample(range(1, len(parent1) - 1), 2))
    child1 = parent1[:points[0]] + parent2[points[0]:points[1]] + parent1[points[1]:]
    child2 = parent2[:points[0]] + parent1[points[0]:points[1]] + parent2[points[1]:]
    return child1, child2

# 变异
def mutate(individual, mutation_rate=0.01):
    '''Let every single point of the chromosome have the same possibility to mutate.'''
    individual_list = list(individual)
    for i in range(len(individual_list)):
        if random.random() < mutation_rate:
            individual_list[i] = '1' if individual_list[i] == '0' else '0'
    return ''.join(individual_list)

# 遗传算法主函数
def genetic_algorithm(pop_size=100, generations=100, mutation_rate=0.01, precision=10, crossover_method='single', mutation_method='single'):
    # 初始化种群
    population = [''.join(random.choice('01') for _ in range(precision)) for _ in range(pop_size)]
    
    for generation in range(generations):
        # 计算适应度
        fitnesses = [fitness(individual) for individual in population]
        
        # 选择、交叉、变异
        new_population = []
        for _ in range(pop_size // 2):
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)
            
            if crossover_method == 'single':
                child1, child2 = single_point_crossover(parent1, parent2)
            else:
                child1, child2 = multi_point_crossover(parent1, parent2, population)
            
            if mutation_method == 'single':
                child1 = mutate(child1, mutation_rate)
                child2 = mutate(child2, mutation_rate)
            else:
                child1 = mutate(child1, mutation_rate)
                child2 = mutate(child2, mutation_rate)
            
            new_population.extend([child1, child2])
        
        population = new_population
        
        # 打印当前最佳解
        best_individual = max(population, key=fitness)
        best_fitness = fitness(best_individual)
        
    best_individual = max(population, key=fitness)
    best_fitness = fitness(best_individual)
    return best_individual, best_fitness
sum_single = 0
sum_multi = 0
# 运行遗传算法并比较两种方法的结果
for i in range(100):
    print("Using single-point crossing with single-point mutation:")
    best_individual_single, best_fitness_single = genetic_algorithm(crossover_method='single', mutation_method='single')
    print(f"Best Individual: {best_individual_single}")
    print(f"Best Fitness: {best_fitness_single}")
    print(f"Optimal x: {binary_to_float(best_individual_single, min_val=-1, max_val=2)}")
    sum_single += best_fitness_single

    print("\nUsing multi-point crossing with multi-point mutation:")
    best_individual_multi, best_fitness_multi = genetic_algorithm(crossover_method='multi', mutation_method='multi')
    print(f"Best Individual: {best_individual_multi}")
    print(f"Best Fitness: {best_fitness_multi}")
    print(f"Optimal x: {binary_to_float(best_individual_multi, min_val=-1, max_val=2)}")
    sum_multi += best_fitness_multi

print(f"Average fitness using single-point crossing with single-point mutation: {sum_single / 100}")
print(f"Average fitness using multi-point crossing with multi-point mutation: {sum_multi / 100}")

