import random
# Using Genetic Algorithm to solve the knapsack problem
V = [0.1, 1, 0.2, 10,  2,  5, 2,  3,  1,  4,  6] # The weight of each item
W = [10, 20,  50, 40, 20, 20, 5, 15, 40, 25, 15] # The value of each item

# Define 50 individuals
def generate_population(pop_size=50):
    population = []
    for i in range(pop_size):
        individual = []
        for j in range(11):
            individual.append(random.randint(0, 1))
        population.append(individual)
    return population




