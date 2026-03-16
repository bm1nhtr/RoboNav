"""
genetic.py — Algorithme genetique pour la recherche de chemin.

Principe
--------
Un algorithme genetique fait evoluer une population d'individus
(sequences de mouvements) sur plusieurs generations afin de minimiser
une fonction de fitness.

Cycle d'evolution
-----------------
1. Initialisation  — creation d'une population aleatoire.
2. Evaluation      — calcul du score fitness de chaque individu.
3. Selection       — conservation des meilleurs individus.
4. Croisement      — generation d'enfants a partir de deux parents.
5. Mutation        — modification aleatoire de certains mouvements.
6. Repetition      — retour a l'etape 2 jusqu'a convergence ou arrivee atteinte.

Fonction de fitness
-------------------
    fitness(chemin) = distance_manhattan(dernier_noeud, arrivee)
                    + 0.1 * longueur_du_chemin

    On penalise les chemins trop longs pour favoriser des solutions concises.

Parametres par defaut
---------------------
    pop_size    = 50   individus par generation
    steps       = 20   mouvements par individu
    generations = 100  nombre de generations

Interface publique
------------------
    genetic_search(grille, depart, arrivee) -> chemin

    Signature compatible avec le pipeline de ``main.py``.
"""

import random

# Mouvements cardinaux possibles : droite, gauche, bas, haut
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ── Heuristique ────────────────────────────────────────────────────────────────

def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Distance de Manhattan entre deux positions.

    Parametres
    ----------
    a, b : tuple[int, int]
        Coordonnees ``(x, y)`` dans la grille.

    Retourne
    --------
    int
        ``|ax - bx| + |ay - by|``
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ── Construction du chemin ────────────────────────────────────────────────────

def apply_moves(
    start:  tuple[int, int],
    moves:  list[tuple[int, int]],
    grid:   list[list[str]],
) -> list[tuple[int, int]]:
    """Appliquer une sequence de mouvements depuis *start* pour construire un chemin.

    Les mouvements qui sortent de la grille ou tombent sur un obstacle
    sont ignores silencieusement.

    Parametres
    ----------
    start : tuple[int, int]
        Position initiale ``(x, y)``.
    moves : list[tuple[int, int]]
        Sequence de deplacements ``(dx, dy)`` a appliquer.
    grid : list[list[str]]
        Grille 2D indexee comme ``grid[y][x]``.

    Retourne
    --------
    list[tuple[int, int]]
        Chemin construit, incluant *start*.
    """
    x, y = start
    path = [start]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        # Verifier les limites de la grille et l'absence d'obstacle
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != "X":
                x, y = nx, ny
                path.append((x, y))

    return path


# ── Fitness ───────────────────────────────────────────────────────────────────

def fitness(path: list[tuple[int, int]], goal: tuple[int, int]) -> float:
    """Evaluer la qualite d'un chemin (plus le score est bas, meilleur est le chemin).

    Parametres
    ----------
    path : list[tuple[int, int]]
        Chemin construit par ``apply_moves``.
    goal : tuple[int, int]
        Coordonnees ``(x, y)`` de l'arrivee.

    Retourne
    --------
    float
        Score = distance_manhattan(derniere_case, arrivee) + 0.1 * longueur.
        Un score de 0 signifie que l'arrivee est atteinte avec le chemin minimal.
    """
    last = path[-1]
    distance = heuristic(last, goal)
    # Penalite sur la longueur pour decourager les chemins inutilement longs
    return distance + 0.1 * len(path)


# ── Operateurs genetiques ─────────────────────────────────────────────────────

def random_individual(length: int) -> list[tuple[int, int]]:
    """Creer un individu aleatoire (sequence de mouvements).

    Parametres
    ----------
    length : int
        Nombre de mouvements dans l'individu.

    Retourne
    --------
    list[tuple[int, int]]
        Sequence de *length* deplacements choisis aleatoirement dans MOVES.
    """
    return [random.choice(MOVES) for _ in range(length)]


def mutate(
    individual: list[tuple[int, int]],
    rate: float = 0.1,
) -> list[tuple[int, int]]:
    """Muter un individu en remplacant aleatoirement certains mouvements.

    Parametres
    ----------
    individual : list[tuple[int, int]]
        Sequence de mouvements a muter.
    rate : float
        Probabilite de mutation par mouvement (defaut : 10 %).

    Retourne
    --------
    list[tuple[int, int]]
        Nouvel individu mute (l'original n'est pas modifie).
    """
    return [
        random.choice(MOVES) if random.random() < rate else move
        for move in individual
    ]


def crossover(
    parent1: list[tuple[int, int]],
    parent2: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Croisement monopoint entre deux parents pour produire un enfant.

    Parametres
    ----------
    parent1, parent2 : list[tuple[int, int]]
        Sequences de mouvements des deux parents.

    Retourne
    --------
    list[tuple[int, int]]
        Enfant constitue du debut de *parent1* et de la fin de *parent2*.
    """
    cut = random.randint(0, len(parent1) - 1)
    return parent1[:cut] + parent2[cut:]


# ── Algorithme genetique principal ────────────────────────────────────────────

def genetic_search(
    grid:        list[list[str]],
    start:       tuple[int, int],
    goal:        tuple[int, int],
    pop_size:    int   = 50,
    steps:       int   = 20,
    generations: int   = 100,
) -> list[tuple[int, int]]:
    """Trouver un chemin de *start* a *goal* par algorithme genetique.

    Parametres
    ----------
    grid : list[list[str]]
        Grille 2D indexee comme ``grid[y][x]``.
    start : tuple[int, int]
        Coordonnees ``(x, y)`` du point de depart.
    goal : tuple[int, int]
        Coordonnees ``(x, y)`` du point d'arrivee.
    pop_size : int
        Nombre d'individus par generation (defaut : 50).
    steps : int
        Nombre de mouvements par individu (defaut : 20).
    generations : int
        Nombre de generations d'evolution (defaut : 100).

    Retourne
    --------
    list[tuple[int, int]]
        Meilleur chemin trouve. Peut ne pas etre optimal selon les parametres.
    """
    # Initialisation de la population avec des individus aleatoires
    population = [random_individual(steps) for _ in range(pop_size)]

    for _generation in range(generations):
        # Evaluer chaque individu et construire son chemin
        scored = []
        for individual in population:
            path  = apply_moves(start, individual, grid)
            score = fitness(path, goal)

            # Arret immediat si l'arrivee est atteinte
            if heuristic(path[-1], goal) == 0:
                return path

            scored.append((score, individual))

        # Trier par score croissant (meilleur score = plus bas)
        scored.sort(key=lambda x: x[0])

        # Selection des 10 meilleurs individus (elitisme)
        elite = [ind for _, ind in scored[:10]]

        # Construction de la nouvelle population
        new_population = list(elite)  # on conserve l'elite

        # Completer avec des enfants issus de croisement + mutation
        while len(new_population) < pop_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child   = mutate(crossover(parent1, parent2))
            new_population.append(child)

        population = new_population

    # Aucune solution parfaite trouvee : retourner le meilleur chemin final
    best_individual = min(
        population,
        key=lambda ind: fitness(apply_moves(start, ind, grid), goal),
    )
    return apply_moves(start, best_individual, grid)
