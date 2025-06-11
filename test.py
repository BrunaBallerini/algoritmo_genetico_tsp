import random
from genetic_algorithm import order_crossover, generate_random_population, calculate_fitness, mutate

## demonstration: crossover test code
parent1 = [(1, 1), (2, 2), (3, 3), (4,4), (5,5), (6, 6)]
parent2 = [(6, 6), (5, 5), (4, 4), (3, 3),  (2, 2), (1, 1)]

# parent1 = [1, 2, 3, 4, 5, 6]
# parent2 = [6, 5, 4, 3, 2, 1]


child = order_crossover(parent1, parent2)
print("Parent 1:", [0, 1, 2, 3, 4, 5, 6, 7, 8])
print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Child   :", child)


# Example usage:
population = generate_random_population(5, 10)

print(calculate_fitness(population[0]))


population = [(random.randint(0, 100), random.randint(0, 100))
          for _ in range(3)]


## Demonstration: mutation test code    
# Example usage:
original_solution = [(1, 1), (2, 2), (3, 3), (4, 4)]
mutation_probability = 1

mutated_solution = mutate(original_solution, mutation_probability)
print("Original Solution:", original_solution)
print("Mutated Solution:", mutated_solution)