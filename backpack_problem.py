import random
from matplotlib import pyplot as plt

# Using Genetic Algorithm to solve the knapsack problem
# _weights = [0.1, 1, 0.2, 10,  2,  5, 2,  3,  1,  4,  6]  # The weight of each item
# _values = [10, 20, 50, 40, 20, 20, 5, 15, 40, 25, 15]  # The value of each item
# _BAG_SIZE = 20

# The data below are generated by knapsack_data_random_generator.py
weights = [7.5803545141190884, 2.8735472988461295, 8.742637711496094, 5.6711287736406035, 1.2181214693906215, 5.845593789945252, 8.541505234747273, 0.3898933119697008, 1.1357756095784373, 8.318198575784484, 5.75324523765078, 2.246898369384598, 4.279166422043562, 9.37283382064634, 9.195652753529236, 8.609717866070001, 8.27105998967943, 9.329125083881278, 3.9429328451429977, 6.626084674247363, 7.658394475605123, 7.738479052184819, 1.5336498537944345, 5.975131253784661, 6.293716536072108, 4.239442662046097, 8.969504204443092, 4.486404182268783, 6.946983974588348, 2.898536651868776, 3.9534605010688706, 2.214976857097552, 2.501980450009311, 8.756860921926878, 1.3551751080863172, 4.583679592820634, 1.0654834078953836, 0.19516862806817792, 3.346560018654652, 2.335221050164575, 6.844660606331323, 4.203269102806347, 2.018654744187463, 1.8085594043744349, 7.384584005585192, 8.777405314360625, 4.004504389401671, 0.35752254666659944, 0.5097987913743903, 1.145429470924196, 2.0282344523843614, 4.594678458128818, 2.2887037002306494, 0.35016368090386973, 7.319013648122511, 4.83448760343127, 4.99689188816923, 0.5539979755503467, 0.48179507172667746, 3.4479218560726794, 6.076354251536907, 9.84954133483895, 3.5513288440572794, 2.4543048958659486, 2.8310173315684346, 8.523000501858423, 8.221310176866698, 4.632292873838816, 4.8260669497572755, 4.476780982554379, 1.095994879924392, 7.417248272439312, 1.4128844219904155, 6.130407426150281, 7.9951133787486794, 5.387132973712897, 2.612773641800109, 1.8552875078382314, 3.092377201913378, 1.6488630542444531, 7.88896077404698, 7.300868507181597, 7.887064405170774, 8.701712409945735, 3.5172604010013955, 4.311515936944818, 2.7223907549958537, 6.844601219672905, 9.849995643256875, 0.8633306787225694, 0.1566545293184649, 1.280745878372985, 5.392236652190189, 3.9617136878789543, 5.339462063319687, 4.947138898602936, 9.338425930621309, 9.940805855052275, 6.528638708271107, 2.889616639310508]
values = [41, 31, 68, 43, 2, 20, 30, 60, 41, 44, 19, 24, 17, 23, 21, 25, 12, 3, 66, 2, 62, 13, 29, 22, 57, 62, 15, 1, 67, 11, 39, 36, 5, 35, 57, 27, 38, 68, 35, 39, 59, 20, 3, 44, 15, 24, 35, 2, 54, 40, 64, 59, 26, 62, 44, 52, 9, 14, 49, 37, 56, 17, 62, 6, 22, 5, 8, 9, 16, 60, 38, 52, 43, 49, 52, 65, 45, 2, 30, 12, 33, 20, 47, 11, 13, 48, 17, 54, 13, 34, 10, 20, 39, 35, 11, 35, 42, 37, 38, 34]
BAG_SIZE = 50
MUTATION_RATE = .01
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
def fitness(individual):
    weight = 0
    value = 0
    for i in range(11):
        if individual[i]:
            weight += weights[i]
            value += values[i]
    if weight <= BAG_SIZE:
        return value
    else:
        return -value
# Selection function - Roulette Wheel Selection
def select_roulette_wheel(population):
    fitness_scores = [fitness(individual) for individual in population]
    total_fitness = sum(max(0, score) for score in fitness_scores)  # Only calculate non-negative fitnesses
    selection_probs = [max(0, score) / total_fitness for score in fitness_scores]
    selected_indices = random.choices(range(len(population)), weights=selection_probs, k=len(population))
    return [population[i] for i in selected_indices]

# Selection function - Tournament Selection
def select_tournament(population, tournament_size=5):
    selected_population = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        selected_population.append(max(tournament, key=fitness))
    return selected_population

# Crossover function
def crossover(parent1, parent2):
    point = random.randint(1, 10)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutation function - Single Point Mutation
def mutation_single_point(pop):
    genNum = len(weights)
    res = []
    for s in pop:
        if (random.random() < MUTATION_RATE):
            p = random.randint(0, genNum - 1)
            a = 0 if s[p] == 1 else 1
            s = s[:p] + [a] + s[p+1:]
        res.append(s)
    return res

# Mutation function - Multi Point Mutation
def mutation_multi_point(pop, num_points=2):
    genNum = len(weights)
    res = []
    for s in pop:
        if (random.random() < MUTATION_RATE):
            points = random.sample(range(genNum), num_points)
            for p in points:
                s[p] = 0 if s[p] == 1 else 1
        res.append(s)
    return res

# Genetic algorithm with different parameters
def genetic_algorithm(generations, selection_func, mutation_func, mutation_rate):
    population = generate_population(50)
    best_fitnesses = []
    average_fitnesses = []
    for _ in range(generations):
        population = selection_func(population)
        new_population = []
        while len(new_population) < len(population):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])
        population = mutation_func(new_population)
        valid_population = [individual for individual in population if fitness(individual) >= 0]
        if valid_population:
            best_individual = max(valid_population, key=fitness)
        else:
            best_individual = max(population, key=fitness)
        best_fitnesses.append(fitness(best_individual))
        average_fitnesses.append(sum(fitness(individual) for individual in population) / len(population))
    return best_individual, fitness(best_individual), best_fitnesses, average_fitnesses

result = genetic_algorithm(100, select_roulette_wheel, mutation_single_point, 0.01)
print("Best individual:", result[0])
print("Fitness:", result[1])


# Plotting the best fitness over generations
plt.plot(range(1, 101), result[2])  
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Best Fitness Over Generations')  
plt.show()  

# Define different selection, mutation functions and mutation rates
selection_functions = [select_roulette_wheel, select_tournament]
mutation_functions = [mutation_single_point, mutation_multi_point]
mutation_rates = [0.01, 0.05, 0.1]

# Run genetic algorithm with different parameters and find the best configuration
best_config = None
best_last_fitness = -float('inf')
best_average_fitness = -float('inf')

for selection_func in selection_functions:
    for mutation_func in mutation_functions:
        for mutation_rate in mutation_rates:
            MUTATION_RATE = mutation_rate
            result = genetic_algorithm(100, selection_func, mutation_func, mutation_rate)
            last_fitness = result[1]
            average_fitness = sum(result[3]) / len(result[3])
            if last_fitness > best_last_fitness or (last_fitness == best_last_fitness and average_fitness > best_average_fitness):
                best_config = (selection_func.__name__, mutation_func.__name__, mutation_rate)
                best_last_fitness = last_fitness
                best_average_fitness = average_fitness

            # Plotting the best fitness over generations for each configuration
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.plot(range(1, 101), result[2])
            plt.xlabel('Generation')
            plt.ylabel('Best Fitness')
            plt.title(f'Best Fitness Over Gen - {selection_func.__name__}_{mutation_func.__name__}, Mut Rate: {mutation_rate}')

            # Plotting the average fitness over generations for each configuration
            plt.subplot(1, 2, 2)
            plt.plot(range(1, 101), result[3])
            plt.xlabel('Generation')
            plt.ylabel('Average Fitness')
            plt.title(f'Avg Fitness Over Gen - {selection_func.__name__}_{mutation_func.__name__}, Mut Rate: {mutation_rate}')

            plt.tight_layout()
            plt.show()

# Output the best configuration
print("Best Configuration:")
print(f"Selection Method: {best_config[0]}")
print(f"Mutation Method: {best_config[1]}")
print(f"Mutation Rate: {best_config[2]}")
print(f"Best Fitness: {best_last_fitness}")
print(f"Average Fitness: {best_average_fitness}")

# Plotting the best fitness over generations for the best configuration
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(range(1, 101), result[2])
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title(f'Best Fitness Over Gen - {best_config[0]}_{best_config[1]}, Mut Rate: {best_config[2]}')

# Plotting the average fitness over generations for the best configuration
plt.subplot(1, 2, 2)
plt.plot(range(1, 101), result[3])
plt.xlabel('Generation')
plt.ylabel('Average Fitness')
plt.title(f'Avg Fitness Over Gen - {best_config[0]}_{best_config[1]}, Mut Rate: {best_config[2]}')

plt.tight_layout()
plt.show()