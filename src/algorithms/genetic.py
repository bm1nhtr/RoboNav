import random

# les mouvements possibles du robot (droite, gauche, en bas, enhaut)
MOVES = [(1,0),(-1,0),(0,1),(0,-1)]


# calcule de la distance de Manhattan entre deux positions
def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


# applique une liste de mouvements à partir du start pour construire un chemin
def apply_moves(start, moves, grid):
    x = start[0]
    y = start[1]
    path = [start]

    for move in moves:
        dx = move[0]
        dy = move[1]

        nx = x + dx
        ny = y + dy

        # vérifie que le robot reste dans la grille
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            # vérifie qu'il n'y a pas d'obstacle
            if grid[ny][nx] != "X":
                x = nx
                y = ny
                path.append((x,y))

    return path


# fonction de fitness : évalue la qualité d'un chemin
def fitness(path, goal):
    last = path[-1]
    distance = heuristic(last,goal)
    return distance + 0.1 * len(path)# ici on ajoute une poenalité aux chemin trop longs


# crée un individu aléatoire qui a ses mouvements aléatoires
def random_individual(length):
    individual = []
    for i in range(length):
        move = random.choice(MOVES)
        individual.append(move)

    return individual


# mutation : modifie aléatoirement certains mouvements
def mutate(individual, rate=0.1):
    new = individual[:]
    for i in range(len(new)):
        r = random.random()
        if r < rate:
            new[i] = random.choice(MOVES)
    return new


# crossover : mélange deux individus pour créer un enfant
def crossover(p1,p2):
    cut = random.randint(0,len(p1)-1)
    child = []

    for i in range(cut):
        child.append(p1[i])

    for i in range(cut,len(p2)):
        child.append(p2[i])

    return child


# fonction principale de l'algorithme génétique
def genetic_search(grid,start,goal,pop_size=50,steps=20,generations=100):

    # on créé la population initial
    population = []
    for i in range(pop_size):
        individual = random_individual(steps)
        population.append(individual)


    # évolution sur plusieurs générations 
    for g in range(generations):
        scored = []
        # évaluation de chaque individu
        for individual in population:
            path = apply_moves(start,individual,grid)
            score = fitness(path,goal)
            # si un chemin atteint le goal on peut s'arrêter
            if heuristic(path[-1],goal) == 0:
                return path
            scored.append((score,individual))

        # tri des individus selon leur score
        scored.sort()

        # sélection des meilleurs individus
        best = []

        for i in range(10):
            best.append(scored[i])


        # création d'une nouvelle population 
        new_population = []
        # on garde les meilleurs individus
        for elem in best:
            new_population.append(elem[1])


        # on génère le reste avec crossover + mutation
        while len(new_population) < pop_size:
            parent1 = random.choice(best)[1]
            parent2 = random.choice(best)[1]

            child = crossover(parent1,parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    # choix du meilleur individu final
    best_individual = population[0]
    best_score = fitness(apply_moves(start,best_individual,grid),goal)

    for individual in population:
        path = apply_moves(start,individual,grid)
        score = fitness(path,goal)

        if score < best_score:
            best_score = score
            best_individual = individual

    return apply_moves(start,best_individual,grid)
