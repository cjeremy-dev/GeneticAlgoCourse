import random
import matplotlib.pyplot as plt

# Using Genetic Algorithm to solve the knapsack problem
weights = [7.5803545141190884, 2.8735472988461295, 8.742637711496094, 5.6711287736406035, 1.2181214693906215, 5.845593789945252, 8.541505234747273, 0.3898933119697008, 1.1357756095784373, 8.318198575784484, 5.75324523765078, 2.246898369384598, 4.279166422043562, 9.37283382064634, 9.195652753529236, 8.609717866070001, 8.27105998967943, 9.329125083881278, 3.9429328451429977, 6.626084674247363, 7.658394475605123, 7.738479052184819, 1.5336498537944345, 5.975131253784661, 6.293716536072108, 4.239442662046097, 8.969504204443092, 4.486404182268783, 6.946983974588348, 2.898536651868776, 3.9534605010688706, 2.214976857097552, 2.501980450009311, 8.756860921926878, 1.3551751080863172, 4.583679592820634, 1.0654834078953836, 0.19516862806817792, 3.346560018654652, 2.335221050164575, 6.844660606331323, 4.203269102806347, 2.018654744187463, 1.8085594043744349, 7.384584005585192, 8.777405314360625, 4.004504389401671, 0.35752254666659944, 0.5097987913743903, 1.145429470924196, 2.0282344523843614, 4.594678458128818, 2.2887037002306494, 0.35016368090386973, 7.319013648122511, 4.83448760343127, 4.99689188816923, 0.5539979755503467, 0.48179507172667746, 3.4479218560726794, 6.076354251536907, 9.84954133483895, 3.5513288440572794, 2.4543048958659486, 2.8310173315684346, 8.523000501858423, 8.221310176866698, 4.632292873838816, 4.8260669497572755, 4.476780982554379, 1.095994879924392, 7.417248272439312, 1.4128844219904155, 6.130407426150281, 7.9951133787486794, 5.387132973712897, 2.612773641800109, 1.8552875078382314, 3.092377201913378, 1.6488630542444531, 7.88896077404698, 7.300868507181597, 7.887064405170774, 8.701712409945735, 3.5172604010013955, 4.311515936944818, 2.7223907549958537, 6.844601219672905, 9.849995643256875, 0.8633306787225694, 0.1566545293184649, 1.280745878372985, 5.392236652190189, 3.9617136878789543, 5.339462063319687, 4.947138898602936, 9.338425930621309, 9.940805855052275, 6.528638708271107, 2.889616639310508]
values = [41, 31, 68, 43, 2, 20, 30, 60, 41, 44, 19, 24, 17, 23, 21, 25, 12, 3, 66, 2, 62, 13, 29, 22, 57, 62, 15, 1, 67, 11, 39, 36, 5, 35, 57, 27, 38, 68, 35, 39, 59, 20, 3, 44, 15, 24, 35, 2, 54, 40, 64, 59, 26, 62, 44, 52, 9, 14, 49, 37, 56, 17, 62, 6, 22, 5, 8, 9, 16, 60, 38, 52, 43, 49, 52, 65, 45, 2, 30, 12, 33, 20, 47, 11, 13, 48, 17, 54, 13, 34, 10, 20, 39, 35, 11, 35, 42, 37, 38, 34]
BAG_SIZE = 50

# Define 50 individuals
def generate_population(pop_size=50):
    population = []
    for _ in range(pop_size):
        individual = []
        for _ in range(len(weights)):
            individual.append(random.randint(0, 1))
        population.append(individual)
    return population

# Calculate the fitness of each individual
def fitness(individual, penalty_factor=1000):
    weight = sum(weights[i] for i in range(len(weights)) if individual[i])
    value = sum(values[i] for i in range(len(values)) if individual[i])
    
    if weight > BAG_SIZE:
        # 对超重个体进行惩罚，但不使其适应度为负值
        return value - penalty_factor * (weight - BAG_SIZE)
    else:
        return value

# Selection function
def select(population):
    fitness_scores = [fitness(individual) for individual in population]
    valid_population = [individual for individual, score in zip(population, fitness_scores) if score >= 0]
    
    if not valid_population:
        # 如果没有有效的个体，随机选择个体
        return random.sample(population, len(population))
    
    total_fitness = sum(score for score in fitness_scores if score >= 0)  # 只计算非负适应度
    if total_fitness == 0:
        # 如果总适应度为零，随机选择个体
        return random.sample(population, len(population))
    
    selection_probs = [max(0, score) / total_fitness for score in fitness_scores]
    selected_indices = random.choices(range(len(population)), weights=selection_probs, k=len(population))
    return [population[i] for i in selected_indices]

# Crossover function
def crossover(parent1, parent2):
    point = random.randint(1, len(weights) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutation function
def mutation(pop):
    genNum = len(weights)
    res = []
    for s in pop:
        if (random.random() < 0.01):
            p = random.randint(0, genNum - 1)
            a = 0 if s[p] == 1 else 1
            s = s[:p] + [a] + s[p+1:]
        res.append(s)
    return res

# Genetic algorithm
def genetic_algorithm(generations):
    population = generate_population(50)
    best_fitness_history = []
    for _ in range(generations):
        population = select(population) 
        new_population = []
        while len(new_population) < len(population):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])
        population = mutation(new_population)  
        valid_population = [individual for individual in population if fitness(individual) >= 0]
        if valid_population:
            best_individual = max(valid_population, key=fitness)
        else:
            best_individual = max(population, key=fitness)
        best_fitness = fitness(best_individual)
        best_fitness_history.append(best_fitness)
    return best_individual, best_fitness, best_fitness_history

def read_world_record():
    try:
        with open("world_record.txt", "r") as f:
            lines = f.readlines()
            if len(lines) == 2:
                current_best_fitness = int(lines[0].strip())
                current_best_individual = list(map(int, lines[1].strip().split()))
                return current_best_fitness, current_best_individual
            else:
                return 0, []
    except FileNotFoundError:
        return 0, []

def update_world_record(best_fitness, best_individual):
    with open("world_record.txt", "w") as f:
        f.write(f"{best_fitness}\n")
        f.write(" ".join(map(str, best_individual)))

current_best_fitness, current_best_individual = read_world_record()
result = genetic_algorithm(100)
print("Best individual:", result[0])
print("Fitness:", result[1])

if result[1] > current_best_fitness:
    print("New world record!")
    update_world_record(result[1], result[0])
    print("World record updated.")
else:
    pass

# Plotting the best fitness over generations
plt.plot(range(1, 101), result[2])
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Best Fitness over Generations')
plt.grid(True)
plt.show()