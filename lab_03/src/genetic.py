import pygad
import numpy as np
x = []
y = []
def fitness_func(ga_instance, solution, solution_idx):
    coefficients = np.array(solution)
    predicted_values = np.polyval(coefficients, x)
    fitness = np.mean(np.abs(predicted_values - y))
    return 1 / fitness

def RunGA(xv, yv, dimension, iters = 500):
    global x
    global y
    x = xv
    y = yv

    num_generations = iters
    num_parents_mating = 10
    fitness_function = fitness_func
    sol_per_pop = 20
    num_genes = dimension

    parent_selection_type = "sss"
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_percent_genes = 40
    parent_selection_type = "sss"
    keep_parents = 1

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           parent_selection_type=parent_selection_type,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           keep_parents=keep_parents)

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    return solution

