import random
import math

# 数据
num = 100  # 货物数量
volumes = [1, 86, 87, 8, 1, 2, 3, 1, 88, 8, 10, 1, 39, 3, 4, 3, 5, 7, 4, 6, 5,
           5, 99, 5, 6, 59, 9, 99, 6, 3, 4, 2, 1, 3, 5, 99, 6, 69, 89, 59, 69, 2,
           79, 99, 5, 19, 7, 5, 10, 69, 49, 69, 9, 7, 2, 4, 3, 7, 5, 4, 5, 10, 2,
           1, 4, 10, 9, 6, 10, 10, 10, 2, 10, 2, 4, 6, 4, 1, 7, 6, 1, 10, 1, 3, 4,
           1, 7, 3, 6, 5, 3, 10, 6, 8, 1, 6, 4, 4, 10, 3]  # 体积
V = 127  # 箱子容积

# GA参数
generations = 500  # 迭代次数
popsize = 40  # 种群生物数
teams = 4  # 锦标赛小组队员数
pm = 0.1  # 突变率


def fitness(genome):
    boxes, box, used, box_num = [], [], 0, 0  # Initialize variables
    for item in genome:
        if used + volumes[item] > V:  # If adding item exceeds bin capacity
            boxes.append(sorted(box))  # Close current bin
            box, used, box_num = [], 0, box_num + 1  # Open new bin
        box.append(item)  # Add item to current bin
        used += volumes[item]  # Update used space
    boxes.append(sorted(box))  # Add last bin
    total_volume = sum(volumes)
    used_space = used + box_num * V
    fitness_score = total_volume / used_space if used_space > 0 else 0  # Ensure fitness score is not greater than 1
    return round(fitness_score, 4), boxes  # Return rounded fitness score and list of bins


def generate_population(pop_size=50):
    population = []
    for _ in range(pop_size):
        genome = list(range(len(volumes)))
        random.shuffle(genome)
        population.append(genome)
    return population


def crossover(parent1, parent2):
    size = len(parent1)
    cxpoint1 = random.randint(1, size - 2)
    cxpoint2 = random.randint(cxpoint1 + 1, size - 1)

    child1 = parent1[:cxpoint1] + parent2[cxpoint1:cxpoint2] + parent1[cxpoint2:]
    child2 = parent2[:cxpoint1] + parent1[cxpoint1:cxpoint2] + parent2[cxpoint2:]

    # Ensure no duplicates in the children
    child1 = repair(child1)
    child2 = repair(child2)

    return child1, child2


def repair(child):
    seen = set()
    duplicates = set()
    for item in child:
        if item in seen:
            duplicates.add(item)
        seen.add(item)

    missing_items = set(range(len(volumes))) - seen
    if not missing_items:
        # If there are no missing items, shuffle the child to ensure uniqueness
        random.shuffle(child)
        return child

    for i in range(len(child)):
        if child[i] in duplicates:
            if missing_items:
                child[i] = missing_items.pop()
            else:
                # If there are no missing items, shuffle the child to ensure uniqueness
                random.shuffle(child)
                return child

    return child


def mutation(pop, pm):
    for i in range(len(pop)):
        if random.random() < pm:
            index1, index2 = random.sample(range(len(pop[i])), 2)
            pop[i][index1], pop[i][index2] = pop[i][index2], pop[i][index1]  # Swap two items to avoid duplicates
    return pop


def tournament_selection(population, fitness_scores, teams):
    selected = []
    for _ in range(len(population)):
        tournament_indices = random.sample(range(len(population)), teams)
        winner_index = max(tournament_indices, key=lambda i: fitness_scores[i])
        selected.append(population[winner_index])
    return selected


def genetic_algorithm(generations=1000, pop_size=50, teams=4, pm=0.05):
    population = generate_population(pop_size)
    for gen in range(generations):
        fitness_scores = [fitness(individual)[0] for individual in population]  # Extract only the fitness score
        population = tournament_selection(population, fitness_scores, teams)
        new_population = []
        while len(new_population) < len(population):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])
        population = mutation(new_population[:len(population)], pm)
        valid_population_with_scores = [(individual, fitness(individual)[0]) for individual in population if fitness(individual)[0] >= 0]
        if valid_population_with_scores:
            best_individual, best_fitness = max(valid_population_with_scores, key=lambda x: x[1])
            best_boxes = fitness(best_individual)[1]
            print(f"Generation {gen}: Best Fitness = {best_fitness:.4f}")
            if best_fitness == 1.0:
                print(f"Solution found in generation {gen}")
                print(f"The best box is {best_boxes}")
                break
            print(f"Best Boxes: {best_boxes}")
    return best_individual, best_fitness, best_boxes


if __name__ == "__main__":
    print("理论最少箱子数:", math.ceil(sum(volumes) / V))
    best_individual, best_fitness, best_boxes = genetic_algorithm(generations, popsize, teams, pm)
    print("各箱子装物情况：", best_boxes)
    print("各箱子占用情况：")
    for b in best_boxes:
        total = 0
        for i in b:
            total += volumes[i]
        print(total)