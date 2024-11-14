import random

# Using Genetic Algorithm to solve the knapsack problem
weights = [0.1, 1, 0.2, 10,  2,  5, 2,  3,  1,  4,  6] # The weight of each item
values = [10, 20,  50, 40, 20, 20, 5, 15, 40, 25, 15] # The value of each item

# Define 50 individuals
def generate_population(pop_size=50):
    population = []
    for _ in range(pop_size):
        individual = []
        for _ in range(11):
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
    if weight <= 20:
        return value
    else:
        return -value
    
population = generate_population(50)
fitness_per_pop = [fitness(individual) for individual in population]
world_record_best = 0
with open("world_record.txt", "r") as f:
    world_record_best = int(f.readline())

sorted_pop = sorted(zip(fitness_per_pop, population), reverse=True)

for i in range(50):
    print("\033[31m" if fitness(sorted_pop[i][1])<0 else "\033[32m", sorted_pop[i][1], " has a fitness of ", fitness(sorted_pop[i][1]), "\033[0m")
    if(fitness(sorted_pop[i][1]) > world_record_best):
        world_record_best = fitness(sorted_pop[i][1])
        with open("world_record.txt", "w") as f:
            f.write(str(world_record_best))

