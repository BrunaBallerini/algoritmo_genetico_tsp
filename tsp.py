import pygame # type: ignore
from pygame.locals import * # type: ignore
import random
import itertools
from genetic_algorithm import *
from draw_functions import draw_paths, draw_plot, draw_cities
import sys
import numpy as np # type: ignore
import pygame # type: ignore
from benchmark_att48 import *

'''
População Gerada Randomicamente: Aumentando a população de 100 para 500 a geração com mesmo sub ótimo foi 3 vezes menor
População Gerada com NN: Com a criação da primeira população com o método nearest neighbour o valor sub ótimo foi atingido na segunda geração
'''

# Constantes
# pygame
WIDTH, HEIGHT = 800, 400
NODE_RADIUS = 10
FPS = 30
PLOT_X_OFFSET = 450

# GA
N_CITIES = 15
POPULATION_SIZE = 100 # Population_size: 100 Routes -> 1 Route: sequence of n_cities
N_GENERATIONS = None
MUTATION_PROBABILITY = 0.5

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Initializando o  problema
# Geração randomica de cidades
cities_locations = [(random.randint(NODE_RADIUS + PLOT_X_OFFSET, WIDTH - NODE_RADIUS), random.randint(NODE_RADIUS, HEIGHT - NODE_RADIUS))
                    for _ in range(N_CITIES)]


# Geração Default: 10, 12 or 15
# cities_locations = DEFAULT_PROBLEMS[10]


# Using att48 benchmark
# WIDTH, HEIGHT = 1500, 800
# att_cities_locations = np.array(att_48_cities_locations)
# max_x = max(point[0] for point in att_cities_locations)
# max_y = max(point[1] for point in att_cities_locations)
# scale_x = (WIDTH - PLOT_X_OFFSET - NODE_RADIUS) / max_x
# scale_y = HEIGHT / max_y
# cities_locations = [(int(point[0] * scale_x + PLOT_X_OFFSET),
#                      int(point[1] * scale_y)) for point in att_cities_locations]
# target_solution = [cities_locations[i-1] for i in att_48_cities_order]
# fitness_target_solution = calculate_fitness(target_solution)
# print(f"Best Solution: {fitness_target_solution}")
# ----- Using att48 benchmark


# Initializando Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSP Solver using Pygame")
clock = pygame.time.Clock()
generation_counter = itertools.count(start=1)  # Start the counter at 1


# Criando população inicial
# TODO:- use heuristic Convex Hull to initialize
population = generate_random_population(cities_locations, POPULATION_SIZE)

# population_indexs = generate_nearest_neighbour_population(cities_locations, POPULATION_SIZE)
# population = indices_to_coordinates(population_indexs, cities_locations)

best_fitness_values = []
best_solutions = []
best_global_fitness = float('inf')
best_global_solution = None
best_individual = None


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    generation = next(generation_counter)

    screen.fill(WHITE)

    population_fitness = [calculate_fitness(
        individual) for individual in population]

    population, population_fitness = sort_population(
        population,  population_fitness)

    best_fitness = calculate_fitness(population[0])
    best_solution = population[0]

    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    draw_plot(screen, list(range(len(best_fitness_values))),
              best_fitness_values, y_label="Fitness - Distance (pxls)")

    draw_cities(screen, cities_locations, RED, NODE_RADIUS)
    draw_paths(screen, best_solution, BLUE, width=3)
    draw_paths(screen, population[1], rgb_color=(128, 128, 128), width=1)

    print(f"Generation {generation}: Best fitness = {round(best_fitness, 2)}")

    new_population = [population[0]]  # Mantem o melhor indivíduo para a pŕoxima geração: ELITISMO
    # new_population = [] # Sem elitismo

    while len(new_population) < POPULATION_SIZE:

        # selection
        # simple selection based on first 10 best solutions
        # parent1, parent2 = random.choices(population[:10], k=2)

        # TODO: implementar o método de seleção por torneio
        # solution based on fitness probability
        probability = 1 / np.array(population_fitness)
        parent1, parent2 = random.choices(population, weights=probability, k=2)

        child1 = order_crossover(parent1, parent2)
        # child1 = order_crossover(parent1, parent1)

        child1 = mutate(child1, MUTATION_PROBABILITY)

        new_population.append(child1)

    population = new_population

# TODO: save the best individual.

    if best_fitness < best_global_fitness:
        best_global_fitness = best_fitness
        best_global_solution = best_solution
        best_individual = population[0]
        print(f"New best solution found: {round(best_global_fitness, 2)}")
    elif best_fitness == best_global_fitness:
        # Pode adicionar um contador aqui para ver quantas gerações sem melhoria
        pass


    pygame.display.flip()
    clock.tick(FPS)

# Saindo do software
pygame.quit()
print(f"Best solution: {round(best_global_fitness, 2)}")
print(f"Best population: {best_individual}")
sys.exit()
