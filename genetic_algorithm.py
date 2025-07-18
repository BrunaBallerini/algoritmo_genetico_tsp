import random
import math
import copy 
from typing import List, Tuple

DEFAULT_PROBLEMS = {
5: [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)],
10:[(470, 169), (602, 202), (754, 239), (476, 233), (468, 301), (522, 29), (597, 171), (487, 325), (746, 232), (558, 136)],
12:[(728, 67), (560, 160), (602, 312), (712, 148), (535, 340), (720, 354), (568, 300), (629, 260), (539, 46), (634, 343), (491, 135), (768, 161)],
15:[(512, 317), (741, 72), (552, 50), (772, 346), (637, 12), (589, 131), (732, 165), (605, 15), (730, 38), (576, 216), (589, 381), (711, 387), (563, 228), (494, 22), (787, 288)]
}


def generate_random_population(cities_location: List[Tuple[float, float]], population_size: int) -> List[List[Tuple[float, float]]]:
    """
    Gera uma população aleatória de rotas para uma lista de cidades
    
    Parametros:
    - cities_location (List[Tuple[float, float]]): Lista de tuplas com a localização das cidades
        com latitude e longitude
    - population_size (int): Tamanho da população, ou seja, o número de rotas a serem geradas.

    Returns:
    List[List[Tuple[float, float]]]: Lista de rotas onde cada uma elemento representa uma lista de localização de cidades.
    
    """
    population = []
    for _ in range(population_size):
        shuffled = cities_location.copy()
        random.shuffle(shuffled)
        population.append(shuffled)
    return population


def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calcula a distância Euclidiana de entre dois pontos.

    Parameters:
    - point1 (Tuple[float, float]): Coordenadas do primeiro ponto.
    - point2 (Tuple[float, float]): Coordenadas do segundo ponto.

    Returns:
    float: Distância Euclidiana entre dois pontos.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) # Pode ser utilizado a matriz de distância 


def generate_nearest_neighbour_population(cities_location: List[Tuple[float, float]], population_size: int) -> List[List[Tuple[float, float]]]:
    """
    Gera as rotas com vizinho mais pŕoximos começando por uma cidade randômica.

    Parameters:
    - cities_location: List[Tuple[float, float]]: Lista da posição das cidades.
    - population_size: int: Tamanho da população a ser gerado.

    Returns:
    population_indices: List[List[int]]: Várias listas de soluções NNP com o tamanho da população.
    """
    population_indices = [] # Vetor de preenchimento da minha população

    for _ in range(population_size):
        cities_list_size = len(cities_location) 
        unvisited = set(range(cities_list_size)) # Set com as posições do vetor inicial para verificação de quais foram visitadas
        current = random.choice(list(unvisited)) # Primeira cidade é randômica
        tour = [current] # Rota com a primeira cidade atual
        unvisited.remove(current) # Remove para não passar pela mesma cidade

        while unvisited: # Loop enquanto tiver cidade que não foi visitada
            # min() itera sobre o set unvisited e para cada valor dentro dele city, compara dentro do cities_location qual o 
            # menor valor e trás o índice dentro do set
            next_city = min(unvisited, key=lambda city: calculate_distance(cities_location[current], cities_location[city]))
            tour.append(next_city) # Acrescenta a nova cidade a rota
            unvisited.remove(next_city) # Remove a cidade
            current = next_city # Passa para o próximo passo da rota

        population_indices.append(tour) # Acreescenta a rota dentro de polulação até completar o tamanho escolhido para ela no argumento

    return population_indices


def indices_to_coordinates(population_indices: List[List[int]], cities_location: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
    """Converte uma população de índices para uma população de coordenadas"""
    return [[cities_location[idx] for idx in individual] for individual in population_indices]


def calculate_fitness(path: List[Tuple[float, float]]) -> float:
    """
    Calculate the fitness of a given path based on the total Euclidean distance.

    Parameters:
    - path (List[Tuple[float, float]]): A list of tuples representing the path,
      where each tuple contains the coordinates of a point.

    Returns:
    float: The total Euclidean distance of the path.
    """
    distance = 0
    n = len(path)
    for i in range(n):
        distance += calculate_distance(path[i], path[(i + 1) % n])

    return distance


# TODO: Retornas dois indivíduos filhos
def order_crossover(parent1: List[Tuple[float, float]], parent2: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Perform order crossover (OX) between two parent sequences to create a child sequence.

    Parameters:
    - parent1 (List[Tuple[float, float]]): The first parent sequence.
    - parent2 (List[Tuple[float, float]]): The second parent sequence.

    Returns:
    List[Tuple[float, float]]: The child sequence resulting from the order crossover.
    """
    length = len(parent1)

    # Choose two random indices for the crossover
    start_index = random.randint(0, length - 1)
    end_index = random.randint(start_index + 1, length)

    # Initialize the child with a copy of the substring from parent1
    child = parent1[start_index:end_index]

    # Fill in the remaining positions with genes from parent2
    remaining_positions = [i for i in range(length) if i < start_index or i >= end_index]
    remaining_genes = [gene for gene in parent2 if gene not in child]

    for position, gene in zip(remaining_positions, remaining_genes):
        child.insert(position, gene)

    return child


# TODO: implement a mutation_intensity and invert pieces of code instead of just swamping two. 
def mutate(solution: List[Tuple[float, float]], mutation_probability: float) ->  List[Tuple[float, float]]:
    """
    Mutate a solution by inverting a segment of the sequence with a given mutation probability.

    Parameters:
    - solution (List[int]): The solution sequence to be mutated.
    - mutation_probability (float): The probability of mutation for each individual in the solution.

    Returns:
    List[int]: The mutated solution sequence.
    """
    mutated_solution = copy.deepcopy(solution)

    # Check if mutation should occur    
    if random.random() < mutation_probability:
        
        # Ensure there are at least two cities to perform a swap
        if len(solution) < 2:
            return solution
    
        # Select a random index (excluding the last index) for swapping
        index = random.randint(0, len(solution) - 2)
        
        # Swap the cities at the selected index and the next index
        mutated_solution[index], mutated_solution[index + 1] = solution[index + 1], solution[index]   
        
    return mutated_solution


def sort_population(population: List[List[Tuple[float, float]]], fitness: List[float]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
    """
    Sort a population based on fitness values.

    Parameters:
    - population (List[List[Tuple[float, float]]]): The population of solutions, where each solution is represented as a list.
    - fitness (List[float]): The corresponding fitness values for each solution in the population.

    Returns:
    Tuple[List[List[Tuple[float, float]]], List[float]]: A tuple containing the sorted population and corresponding sorted fitness values.
    """
    # Combine lists into pairs
    combined_lists = list(zip(population, fitness))

    # Sort based on the values of the fitness list
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1])

    # Separate the sorted pairs back into individual lists
    sorted_population, sorted_fitness = zip(*sorted_combined_lists)

    return sorted_population, sorted_fitness


if __name__ == '__main__':
    N_CITIES = 10
    
    POPULATION_SIZE = 100
    N_GENERATIONS = 100
    MUTATION_PROBABILITY = 0.3
    cities_locations = [(random.randint(0, 100), random.randint(0, 100))
              for _ in range(N_CITIES)]
    
    # CREATE INITIAL POPULATION
    population = generate_random_population(cities_locations, POPULATION_SIZE)

    # Lists to store best fitness and generation for plotting
    best_fitness_values = []
    best_solutions = []
    
    for generation in range(N_GENERATIONS):
  
        
        population_fitness = [calculate_fitness(individual) for individual in population]    
        
        population, population_fitness = sort_population(population,  population_fitness)
        
        best_fitness = calculate_fitness(population[0])
        best_solution = population[0]
           
        best_fitness_values.append(best_fitness)
        best_solutions.append(best_solution)    

        # print(f"Generation {generation}: Best fitness = {best_fitness}")

        new_population = [population[0]]  # Keep the best individual: ELITISM
        
        while len(new_population) < POPULATION_SIZE:
            
            # SELECTION
            parent1, parent2 = random.choices(population[:10], k=2)  # Select parents from the top 10 individuals
            
            # CROSSOVER
            child1 = order_crossover(parent1, parent2)
            
            ## MUTATION
            child1 = mutate(child1, MUTATION_PROBABILITY)
            
            new_population.append(child1)
            
    
        # print('generation: ', generation)
        population = new_population
    


