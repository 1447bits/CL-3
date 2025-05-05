import numpy as np

# Objective function (minimize distance from 3)
def objective_function(x):
    return np.sum((x - 3)**2)

# 1. Initialize population (0-10 only)
def initialize_population(pop_size, dim):
    return np.random.uniform(0, 10, (pop_size, dim))

# 2. Calculate fitness
def calculate_fitness(population):
    return np.apply_along_axis(objective_function, 1, population)

# 3. Select top antibodies
def select_antibodies(population, fitness, num_selected):
    sorted_idx = np.argsort(fitness)
    return population[sorted_idx[:num_selected]]

# 4. Clone selected antibodies
def clone_antibodies(selected, clone_factor):
    return np.repeat(selected, clone_factor, axis=0)

# 5. Mutate clones (no negative values)
def mutate_clones(clones, mutation_rate):
    mutations = np.random.uniform(-mutation_rate, mutation_rate, clones.shape)
    mutated = clones + mutations
    return np.clip(mutated, 0, 10)  # Ensure 0-10 range

# 6. Select next generation
def select_next_generation(population, clones, pop_size):
    combined = np.vstack((population, clones))
    combined_fitness = calculate_fitness(combined)
    best_indices = np.argsort(combined_fitness)[:pop_size]
    return combined[best_indices]

# Main algorithm
def clonal_selection(pop_size=50, num_gen=50, dim=5, clone_factor=5, mutation_rate=0.2):
    # Initialize
    pop = initialize_population(pop_size, dim)
    best_sol = None
    best_fit = float('inf')
    
    for _ in range(num_gen):
        # Evaluate
        fitness = calculate_fitness(pop)
        
        # Track best
        if fitness[0] < best_fit:
            best_sol = pop[0].copy()
            best_fit = fitness[0]
        
        # Selection
        selected = select_antibodies(pop, fitness, pop_size//2)
        
        # Cloning
        clones = clone_antibodies(selected, clone_factor)
        
        # Mutation (with 0-10 bounds)
        clones = mutate_clones(clones, mutation_rate)
        
        # Next generation
        pop = select_next_generation(pop, clones, pop_size)
        print(f'Best fitness in generation {_}: {best_fit}')

    
    return best_sol, best_fit

# Run and print results
solution, fitness = clonal_selection()
print('Best Solution:', solution)
print('Fitness:', fitness)
